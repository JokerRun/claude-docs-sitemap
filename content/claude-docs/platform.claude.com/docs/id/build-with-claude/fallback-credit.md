---
source: platform
url: https://platform.claude.com/docs/id/build-with-claude/fallback-credit
fetched_at: 2026-07-01T03:16:45.163402Z
sha256: eabce9eae85ef586a8f31c1ac1d4859016281af8c1811511905cf6c84d18e8d9
---

# Kredit fallback

Hindari membayar biaya prompt-cache dua kali ketika Anda mencoba ulang permintaan Claude Fable 5 yang ditolak pada model lain.

---

Cache prompt bersifat per-model. Ketika Claude Fable 5 menolak sebuah permintaan dan Anda mencoba ulang pada model lain, prefiks percakapan yang sudah di-cache untuk Claude Fable 5 harus ditulis ke dalam cache model baru dari awal. Penulisan cache lebih mahal daripada pembacaan cache. Kredit fallback menghilangkan biaya tambahan tersebut. Penolakan membawa token kredit, Anda menyertakan kembali token tersebut pada percobaan ulang, dan percobaan ulang ditagih seolah-olah percakapan telah berada di model baru sejak awal.

Anda memerlukan halaman ini hanya ketika Anda membangun percobaan ulang sendiri: pada SDK Ruby atau PHP, melalui HTTP mentah, atau dengan logika percobaan ulang kustom. [Fallback sisi server](/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback) dan [middleware SDK](/docs/id/build-with-claude/refusals-and-fallback#client-side-fallback) menerapkan kredit fallback secara otomatis. Jika Anda menggunakan salah satunya, lewati halaman ini.

[Penolakan dan fallback](/docs/id/build-with-claude/refusals-and-fallback) membahas cara mendeteksi penolakan dan memilih pendekatan fallback. [Caching prompt](/docs/id/build-with-claude/prompt-caching) menjelaskan pembacaan cache dan penulisan cache jika istilah tersebut baru bagi Anda.

## Alur dasar

<Steps>
  <Step title="Aktifkan dengan header beta">
    Kirim permintaan yang mungkin ditolak dengan header `anthropic-beta: fallback-credit-2026-06-01`. Header `server-side-fallback-2026-06-01` juga memberikan field yang sama.
  </Step>

  <Step title="Baca dua field dari penolakan">
    Pada penolakan, `stop_details` menyertakan dua field:

    * **`fallback_credit_token`:** string opaque yang merepresentasikan kredit.
    * **`fallback_has_prefill_claim`:** Boolean yang memberi tahu Anda bentuk body percobaan ulang mana yang harus digunakan.

    Keduanya bernilai `null` ketika tidak ada kredit yang tersedia untuk penolakan tersebut.
  </Step>

  <Step title="Bangun percobaan ulang">
    Mulai dari body permintaan yang ditolak. Atur `model` ke model fallback dan tambahkan token sebagai parameter `fallback_credit_token` tingkat atas. Pilih bentuk body dari tabel di bawah.
  </Step>

  <Step title="Kirim percobaan ulang dengan header yang sama">
    Kirim percobaan ulang dengan header beta `fallback-credit-2026-06-01` yang sama. Percobaan ulang memerlukan header tersebut untuk menukarkan token.
  </Step>
</Steps>

Field `fallback_has_prefill_claim` memberi tahu Anda apakah percobaan ulang dapat melanjutkan output parsial dari model yang ditolak alih-alih memulai dari awal:

| `fallback_has_prefill_claim` | Body percobaan ulang                                                                                                                                                                                                                                                                                                                   |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `true`                       | Body permintaan yang ditolak, tanpa perubahan, ditambah satu pesan assistant yang ditambahkan di akhir yang `content`-nya menyalin `content` dari respons yang ditolak. Model percobaan ulang melanjutkan respons dari titik di mana model yang ditolak berhenti, dan panggilan alat server yang telah selesai tidak dieksekusi ulang. |
| `false`                      | Body permintaan yang ditolak, tanpa perubahan.                                                                                                                                                                                                                                                                                         |

## Contoh

Contoh berikut membuat permintaan yang mungkin ditolak dan menukarkan token kredit pada percobaan ulang terhadap Claude Opus 4.8. Ketika upaya percobaan ulang ditolak, contoh ini menurunkan tingkatannya melalui tangga penolakan: urutan bentuk percobaan ulang yang semakin sederhana yang dibahas dalam [Ketika percobaan ulang ditolak](#when-a-retry-is-rejected).

<CodeGroup>
  ```bash cURL
  # Permintaan awal (mungkin ditolak)
  response=$(curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: fallback-credit-2026-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }')

  token=$(jq -r '.stop_details.fallback_credit_token // empty' <<<"$response")

  if [[ -n "$token" ]]; then
    # Coba ulang pada model fallback dengan token kredit (body yang sama)
    response=$(curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: fallback-credit-2026-06-01" \
      -H "content-type: application/json" \
      -d "$(jq -n --arg t "$token" '{
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [{"role": "user", "content": "Hello, Claude"}],
        fallback_credit_token: $t
      }')")
  fi

  # Lihat contoh SDK untuk tangga penanganan penolakan lengkap.
  jq -c '{stop_reason, model}' <<<"$response"
  ```

  ```bash CLI
  # Permintaan awal (mungkin ditolak)
  response=$(ant beta:messages create \
    --model claude-fable-5 \
    --max-tokens 1024 \
    --message '{"role":"user","content":"Hello, Claude"}' \
    --beta fallback-credit-2026-06-01 \
    --format json)

  # Penolakan membawa token kredit sekali pakai di stop_details
  token=$(jq -r '.stop_details.fallback_credit_token // empty' <<<"${response}")

  # Coba ulang pada model fallback dengan token kredit tersebut
  if [[ -n "${token}" ]]; then
    response=$(ant beta:messages create \
      --model claude-opus-4-8 \
      --max-tokens 1024 \
      --message '{"role":"user","content":"Hello, Claude"}' \
      --fallback-credit-token "${token}" \
      --beta fallback-credit-2026-06-01 \
      --format json)
  fi

  jq -c '{stop_reason, model}' <<<"${response}"
  # Lihat contoh SDK untuk tangga penanganan penolakan lengkap.
  ```

  ```python Python
  client = Anthropic()

  request = {
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}],
  }


  def send(model, body):
      return client.beta.messages.create(
          model=model, betas=["fallback-credit-2026-06-01"], **body
      )


  response = send("claude-fable-5", request)

  if (
      response.stop_reason == "refusal"
      and (details := response.stop_details)
      and (token := details.fallback_credit_token)
  ):
      exact_body = request | {"fallback_credit_token": token}
      # Utamakan bentuk kelanjutan kecuali klaimnya False
      if details.fallback_has_prefill_claim is not False:
          # Gemakan konten penolakan, hapus spasi kosong di akhir dari
          # blok teks terakhir (validator prefill menolaknya; pencocokan sisi server
          # menoleransi editan ini). Permintaan yang menggunakan alat juga menghilangkan
          # blok tool_use yang tidak berpasangan, lalu hapus lagi spasi kosong setelah penghilangan.
          echoed = [block.model_dump() for block in response.content]
          match echoed:
              case [*_, {"type": "text"} as final_block]:
                  final_block["text"] = final_block["text"].rstrip()
          attempt = exact_body | {
              "messages": [
                  *request["messages"],
                  {"role": "assistant", "content": echoed},
              ]
          }
      else:
          attempt = exact_body

      try:
          response = send("claude-opus-4-8", attempt)
      except BadRequestError as error:
          if "redemption temporarily unavailable" in str(error):
              raise  # Transient: retry with the token within its five-minute window
          try:
              # Kembali ke isi yang tidak diubah, tetap dengan tokennya
              response = send("claude-opus-4-8", exact_body)
          except BadRequestError as error:
              if "redemption temporarily unavailable" in str(error):
                  raise  # Transient: retry with the token within its five-minute window
              # Token itu sendiri ditolak: lepaskan dan coba lagi tanpanya.
              response = send("claude-opus-4-8", request)

  print(json.dumps({"stop_reason": response.stop_reason, "model": response.model}))
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const request: Anthropic.Beta.MessageCreateParamsNonStreaming = {
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    betas: ["fallback-credit-2026-06-01"]
  };

  let response = await client.beta.messages.create(request);

  if (
    response.stop_reason === "refusal" &&
    response.stop_details?.type === "refusal" &&
    response.stop_details.fallback_credit_token
  ) {
    const { fallback_credit_token, fallback_has_prefill_claim } = response.stop_details;
    const fallbackModel = "claude-opus-4-8";

    const exactRetry: Anthropic.Beta.MessageCreateParamsNonStreaming = {
      ...request,
      model: fallbackModel,
      fallback_credit_token
    };

    // Bentuk terkaya dulu, menurun pada setiap penolakan: bentuk kelanjutan
    // (kecuali klaimnya salah), body yang tidak diubah masih membawa
    // token, dan akhirnya melepaskan token.
    let attempt = exactRetry;
    if (fallback_has_prefill_claim !== false) {
      // Gemakan konten penolakan sebagai giliran asisten, hapus spasi kosong
      // di akhir blok teks terakhir (validator prefill menolaknya; pencocokan
      // sisi server menoleransi editan). Permintaan yang memakai alat juga
      // menghapus blok tool_use tak berpasangan, lalu strip ulang setelahnya.
      const finalIndex = response.content.length - 1;
      const echoed: Anthropic.Beta.BetaContentBlockParam[] = response.content.map(
        (block, index) =>
          block.type === "text" && index === finalIndex
            ? { ...block, text: block.text.trimEnd() }
            : block
      );
      attempt = {
        ...exactRetry,
        messages: [...request.messages, { role: "assistant", content: echoed }]
      };
    }

    try {
      response = await client.beta.messages.create(attempt);
    } catch (error) {
      // Turunkan hanya pada 400 terkait bentuk. "redemption temporarily
      // unavailable" bersifat sementara: coba ulang dengan cara yang sama
      // dalam jendela lima menit token tersebut.
      if (
        !(error instanceof Anthropic.BadRequestError) ||
        error.message.includes("redemption temporarily unavailable")
      ) {
        throw error;
      }
      try {
        response = await client.beta.messages.create(exactRetry);
      } catch (retryError) {
        if (
          !(retryError instanceof Anthropic.BadRequestError) ||
          retryError.message.includes("redemption temporarily unavailable")
        ) {
          throw retryError;
        }
        response = await client.beta.messages.create({ ...request, model: fallbackModel });
      }
    }
  }

  const { stop_reason, model } = response;
  console.log(JSON.stringify({ stop_reason, model }));
  ```

  ```csharp C#
  using Anthropic.Exceptions;
  using Anthropic.Models.Beta.Messages;

  var client = new AnthropicClient();
  const string beta = "fallback-credit-2026-06-01";

  List<BetaMessageParam> requestMessages =
  [
      new() { Role = Role.User, Content = "Hello, Claude" },
  ];
  MessageCreateParams Request(string model) => new()
  {
      Model = model,
      MaxTokens = 1024,
      Messages = requestMessages,
      Betas = [beta],
  };
  var response = await client.Beta.Messages.Create(Request("claude-fable-5"));

  if (
      response.StopReason == BetaStopReason.Refusal
      && response.StopDetails is { FallbackCreditToken: string token } details
  )
  {
      var exactBody = Request("claude-opus-4-8") with { FallbackCreditToken = token };
      var attempt = exactBody;
      // Utamakan bentuk kelanjutan kecuali klaimnya salah
      if (details.FallbackHasPrefillClaim is not false)
      {
          // Gemakan konten penolakan, hapus whitespace di akhir dari
          // blok teks terakhir (validator prefill menolaknya; pencocokan
          // menoleransi editnya). Permintaan yang memakai alat juga menghilangkan blok
          // tool_use tak berpasangan, lalu hapus ulang whitespace setelah penghilangan.
          var echoed = JsonNode.Parse(response.RawData["content"].GetRawText())!.AsArray();
          if (
              echoed is [.., JsonObject lastBlock]
              && lastBlock["type"]?.GetValue<string>() == "text"
              && lastBlock["text"]?.GetValue<string>() is string text
          )
          {
              lastBlock["text"] = text.TrimEnd();
          }
          attempt = exactBody with
          {
              Messages =
              [
                  .. requestMessages,
                  new()
                  {
                      Role = Role.Assistant,
                      Content = new BetaMessageParamContent(
                          JsonSerializer.SerializeToElement(echoed)
                      ),
                  },
              ],
          };
      }
      // Penolakan sementara "redemption temporarily unavailable" merambat keluar dari
      // setiap filter catch berikut: coba lagi dengan token dalam jendela lima menitnya.
      try
      {
          response = await client.Beta.Messages.Create(attempt);
      }
      catch (AnthropicBadRequestException e)
          when (!e.Message.Contains("redemption temporarily unavailable"))
      {
          try
          {
              // Kembali ke body yang tidak diubah, tetap dengan token
              response = await client.Beta.Messages.Create(exactBody);
          }
          catch (AnthropicBadRequestException retryError)
              when (!retryError.Message.Contains("redemption temporarily unavailable"))
          {
              // Token itu sendiri ditolak: lepaskan dan coba lagi tanpanya.
              response = await client.Beta.Messages.Create(Request("claude-opus-4-8"));
          }
      }
  }

  Console.WriteLine(
      JsonSerializer.Serialize(
          new { stop_reason = response.StopReason?.Raw(), model = response.Model.Raw() }
      )
  );
  ```

  ```go Go
  ctx := context.Background()
  client := anthropic.NewClient()

  request := anthropic.BetaMessageNewParams{
  	MaxTokens: 1024,
  	Betas:     []anthropic.AnthropicBeta{"fallback-credit-2026-06-01"},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  }

  send := func(model anthropic.Model, body anthropic.BetaMessageNewParams) (*anthropic.BetaMessage, error) {
  	body.Model = model
  	return client.Beta.Messages.New(ctx, body)
  }
  // Error 400 non-transien berarti bentuk upaya atau token ini ditolak dan
  // anak tangga berikutnya harus dijalankan. "redemption temporarily
  // unavailable" bersifat transien: tampilkan dan coba lagi dengan token dalam
  // jendela lima menitnya.
  canFallBack := func(err error) bool {
  	apiErr, ok := errors.AsType[*anthropic.Error](err)
  	return ok && apiErr.StatusCode == 400 &&
  		!strings.Contains(apiErr.Error(), "redemption temporarily unavailable")
  }

  response, err := send(anthropic.ModelClaudeFable5, request)
  if err != nil {
  	log.Fatal(err)
  }

  if response.StopReason == anthropic.BetaStopReasonRefusal {
  	details := response.StopDetails
  	if token := details.FallbackCreditToken; token != "" {
  		exactBody := request
  		exactBody.FallbackCreditToken = anthropic.String(token)
  		attempt := exactBody
  		// Utamakan bentuk lanjutan kecuali klaimnya salah
  		if details.FallbackHasPrefillClaim || !details.JSON.FallbackHasPrefillClaim.Valid() {
  			// Gema konten penolakan, hapus spasi kosong di akhir dari
  			// blok teks terakhir (validator prefill menolaknya; pencocokan
  			// menoleransi editan). Permintaan yang memakai alat juga menghapus blok
  			// tool_use tak berpasangan, lalu hapus ulang spasi setelah penghapusan.
  			echoed := response.ToParam()
  			if len(echoed.Content) > 0 {
  				if text := echoed.Content[len(echoed.Content)-1].OfText; text != nil {
  					text.Text = strings.TrimRightFunc(text.Text, unicode.IsSpace)
  				}
  			}
  			attempt.Messages = append(slices.Clone(request.Messages), echoed)
  		}
  		response, err = send(anthropic.ModelClaudeOpus4_8, attempt)
  		if err != nil && canFallBack(err) {
  			// Kembali ke body yang tidak diubah, tetap dengan token
  			response, err = send(anthropic.ModelClaudeOpus4_8, exactBody)
  			if err != nil && canFallBack(err) {
  				// Token itu sendiri ditolak: lepaskan dan coba lagi tanpanya.
  				response, err = send(anthropic.ModelClaudeOpus4_8, request)
  			}
  		}
  		if err != nil {
  			log.Fatal(err)
  		}
  	}
  }

  summary, err := json.Marshal(struct {
  	StopReason anthropic.BetaStopReason `json:"stop_reason"`
  	Model      anthropic.Model          `json:"model"`
  }{response.StopReason, response.Model})
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(string(summary))
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams.Builder request() {
      return MessageCreateParams.builder()
          .maxTokens(1024L)
          .addUserMessage("Hello, Claude")
          .addBeta("fallback-credit-2026-06-01");
  }

  BetaMessage send(String model, MessageCreateParams.Builder body) {
      return client.beta().messages().create(body.model(model).build());
  }

  void main() {
      BetaMessage response = send("claude-fable-5", request());

      if (response.stopReason().map(BetaStopReason.REFUSAL::equals).orElse(false)
              && response.stopDetails().orElse(null) instanceof BetaRefusalStopDetails details
              && details.fallbackCreditToken().orElse(null) instanceof String creditToken) {
          MessageCreateParams.Builder attempt = request().fallbackCreditToken(creditToken);
          // Utamakan bentuk kelanjutan kecuali klaimnya salah
          if (details.fallbackHasPrefillClaim().orElse(true)) {
              // Gemakan konten penolakan, hapus spasi kosong di akhir dari
              // blok teks terakhir (validator prefill menolaknya; pencocokan
              // menoleransi editan). Permintaan yang memakai alat juga menghilangkan
              // blok tool_use tak berpasangan, lalu hapus lagi spasi setelah penghilangan.
              List<BetaContentBlockParam> echoed = new ArrayList<>(
                  response.content().stream().map(BetaContentBlock::toParam).toList());
              if (!echoed.isEmpty() && echoed.getLast().isText()) {
                  var lastText = echoed.removeLast().asText();
                  echoed.addLast(BetaContentBlockParam.ofText(
                      lastText.toBuilder().text(lastText.text().stripTrailing()).build()));
              }
              attempt.addAssistantMessageOfBetaContentBlockParams(echoed);
          }
          try {
              response = send("claude-opus-4-8", attempt);
          } catch (BadRequestException badRequest) {
              // Sementara: coba lagi dengan token dalam jendela lima menitnya
              if (badRequest.getMessage().contains("redemption temporarily unavailable")) {
                  throw badRequest;
              }
              try {
                  // Kembali ke body yang tidak diubah, tetap dengan token
                  response = send("claude-opus-4-8", request().fallbackCreditToken(creditToken));
              } catch (BadRequestException retryBadRequest) {
                  if (retryBadRequest.getMessage().contains("redemption temporarily unavailable")) {
                      throw retryBadRequest;
                  }
                  // Token itu sendiri ditolak: lepaskan dan coba lagi tanpanya.
                  response = send("claude-opus-4-8", request());
              }
          }
      }

      IO.println("{\"stop_reason\": \"%s\", \"model\": \"%s\"}"
          .formatted(response.stopReason().orElseThrow(), response.model()));
  }
  ```

  ```php PHP
  $client = new Client();
  $beta = 'fallback-credit-2026-06-01';
  $messages = [['role' => 'user', 'content' => 'Hello, Claude']];

  $send = fn (string $model, array $messages, ?string $token = null) => $client->beta->messages->create(
      maxTokens: 1024,
      messages: $messages,
      model: $model,
      fallbackCreditToken: $token,
      betas: [$beta],
  );
  $response = $send('claude-fable-5', $messages);

  if ($response->stopReason === 'refusal' && $response->stopDetails !== null) {
      $token = $response->stopDetails->fallbackCreditToken;
      if ($token !== null) {
          $attemptMessages = $messages;
          // Utamakan bentuk kelanjutan kecuali klaimnya salah
          if ($response->stopDetails->fallbackHasPrefillClaim !== false) {
              // Gemakan konten penolakan, hapus spasi kosong di akhir dari
              // blok teks terakhir (validator prefill menolaknya; pencocokan
              // menoleransi editan). Permintaan yang memakai alat juga menghilangkan
              // blok tool_use tak berpasangan, lalu hapus ulang spasi setelah penghilangan.
              $echoed = $response->content
                  |> json_encode(...)
                  |> (fn (string $json): array => json_decode($json, associative: true));
              $lastIndex = array_key_last($echoed);
              if ($lastIndex !== null && $echoed[$lastIndex]['type'] === 'text') {
                  $echoed[$lastIndex]['text'] = rtrim($echoed[$lastIndex]['text']);
              }
              $attemptMessages[] = ['role' => 'assistant', 'content' => $echoed];
          }
          // Sementara: coba lagi dengan token dalam jendela lima menitnya
          $isTransientRedemption = fn (BadRequestException $error): bool =>
              str_contains($error->getMessage(), 'redemption temporarily unavailable');
          try {
              $response = $send('claude-opus-4-8', $attemptMessages, $token);
          } catch (BadRequestException $error) {
              if ($isTransientRedemption($error)) {
                  throw $error;
              }
              try {
                  // Kembali ke body yang tidak diubah, tetap dengan token
                  $response = $send('claude-opus-4-8', $messages, $token);
              } catch (BadRequestException $retryError) {
                  if ($isTransientRedemption($retryError)) {
                      throw $retryError;
                  }
                  // Token itu sendiri ditolak: lepaskan dan coba lagi tanpanya.
                  $response = $send('claude-opus-4-8', $messages);
              }
          }
      }
  }

  echo json_encode(['stop_reason' => $response->stopReason, 'model' => $response->model]), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  request = {
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}]
  }

  send_message = lambda do |model, body|
    client.beta.messages.create(model:, betas: ["fallback-credit-2026-06-01"], **body)
  end

  response = send_message.call("claude-fable-5", request)

  if response in {stop_reason: :refusal,
                  stop_details: {fallback_credit_token: String => credit_token} => details}
    exact_body = request.merge(fallback_credit_token: credit_token)

    # Utamakan bentuk lanjutan kecuali klaimnya salah
    if details.fallback_has_prefill_claim != false
      # Gemakan konten penolakan, hapus spasi kosong di akhir dari blok teks
      # terakhir (validator prefill menolaknya; pencocokan menoleransi
      # editan). Permintaan yang memakai alat juga menghilangkan blok tool_use
      # tak berpasangan, lalu menghapus ulang spasi kosong setelah penghilangan.
      echoed = response.content.map(&:to_h)
      if echoed.last in {type: :text, text: String => final_text}
        echoed[-1] = echoed[-1].merge(text: final_text.rstrip)
      end
      attempt = exact_body.merge(
        messages: [*request[:messages], {role: "assistant", content: echoed}]
      )
    else
      attempt = exact_body
    end

    begin
      response = send_message.call("claude-opus-4-8", attempt)
    rescue Anthropic::Errors::BadRequestError => error
      # Sementara: coba lagi dengan token dalam jendela lima menitnya
      raise if error.message.include?("redemption temporarily unavailable")
      begin
        # Kembali ke body yang tidak diubah, tetap dengan token
        response = send_message.call("claude-opus-4-8", exact_body)
      rescue Anthropic::Errors::BadRequestError => error
        # Sementara: coba lagi dengan token dalam jendela lima menitnya
        raise if error.message.include?("redemption temporarily unavailable")
        # Token itu sendiri ditolak: lepaskan dan coba lagi tanpanya.
        response = send_message.call("claude-opus-4-8", request)
      end
    end
  end

  puts JSON.generate({stop_reason: response.stop_reason, model: response.model})
  ```
</CodeGroup>

## Di mana ini berfungsi

Kredit fallback berada dalam tahap beta pada Claude API, Claude Platform di AWS, Amazon Bedrock, Google Cloud, dan Microsoft Foundry. Token kredit yang dikembalikan dalam hasil [Message Batches](/docs/id/build-with-claude/batch-processing) tidak dapat ditukarkan. Penukaran hanya berlaku untuk permintaan Messages API langsung.

Model percobaan ulang harus merupakan salah satu target fallback yang diizinkan dari model yang ditolak. Pada saat peluncuran, target yang diizinkan untuk Claude Fable 5 adalah Claude Opus 4.8 (`claude-opus-4-8`).

<Accordion title="Mencari target fallback yang diizinkan secara terprogram">
  Pada Claude API dan Claude Platform di AWS, daftar target dipublikasikan sebagai `allowed_fallback_models` pada entri setiap model di [Models API](/docs/id/api/models/list) ketika header beta `server-side-fallback-2026-06-01` diatur. Daftar tersebut belum terlihat di bawah header `fallback-credit-*` saja. Daftar ini tidak diekspos pada Amazon Bedrock, Google Cloud, atau Microsoft Foundry.
</Accordion>

## Memeriksa bahwa kredit telah diterapkan

Pengembalian dana terlihat dalam `usage` percobaan ulang. Dibandingkan dengan apa yang akan dilaporkan oleh permintaan yang sama tanpa token, `cache_creation_input_tokens` lebih rendah, dan `cache_read_input_tokens` lebih tinggi dengan jumlah yang sama. Pergeseran sebesar nol berarti token dihormati tetapi tidak ada yang perlu dihargai ulang, misalnya karena cache model percobaan ulang sudah hangat.

## Ketika percobaan ulang ditolak

Sebagian besar percobaan ulang berhasil ditukarkan pada upaya pertama. Ketika tidak berhasil, API mengembalikan error 400 yang memberi tahu Anda apa yang harus dicoba selanjutnya.

<Steps>
  <Step title="Kelanjutan ditolak: kirim ulang body tanpa perubahan">
    Jika percobaan ulang yang menambahkan pesan assistant ditolak dengan error 400, kirim ulang body permintaan yang ditolak tanpa perubahan, tetap dengan token.
  </Step>

  <Step title="Token ditolak: hapus token">
    Jika body tanpa perubahan juga ditolak dengan error 400 yang pesannya menyebutkan `fallback_credit_token`, coba ulang tanpa token. Kredit hangus, tetapi percobaan ulang itu sendiri berhasil diproses.
  </Step>
</Steps>

<Note>
  Jika permintaan yang ditolak mengeksekusi alat server, percobaan ulang tanpa token akan menjalankan ulang dan menagih ulang alat-alat tersebut. Dalam kasus itu, tampilkan error 400 kepada pemanggil Anda alih-alih melanjutkan ke percobaan ulang tanpa token.
</Note>

<Accordion title="Jika error menyatakan 'redemption temporarily unavailable'">
  Penolakan ini bersifat sementara, bukan keputusan final atas bentuk percobaan ulang Anda. Coba ulang permintaan yang sama, dengan token yang sama, dalam jendela lima menit token tersebut. Jangan berpindah ke langkah berikutnya dalam tangga.
</Accordion>

## Referensi

Bagian-bagian di bawah ini membahas kasus-kasus khusus dan aturan penukaran lengkap. Sebagian besar integrasi tidak memerlukannya.

<Accordion title="Field yang harus cocok dengan permintaan yang ditolak">
  Penukaran membandingkan percobaan ulang dengan permintaan yang ditolak. Setiap field yang membentuk prompt harus cocok persis. Field yang tidak membentuk prompt boleh berubah pada percobaan ulang.

  | Aturan                             | Field                                                                                                                                                                                    |
  | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | Harus cocok persis                 | `system`, `messages`, `tools`, `tool_choice`, `thinking`, dan `cache_control`, ditambah `output_config`, `mcp_servers`, `context_management`, dan `container` ketika Anda menggunakannya |
  | Boleh berubah pada percobaan ulang | `model`, `max_tokens`, `stop_sequences`, `temperature`, `top_p`, `top_k`, `stream`, `metadata`, dan `service_tier`                                                                       |

  Bentuk kelanjutan (`fallback_has_prefill_claim: true`) adalah satu-satunya pengecualian untuk kecocokan `messages`: bentuk ini menambahkan tepat satu pesan assistant di akhir `messages`.

  Jangan menghapus blok `thinking` atau `redacted_thinking` dari giliran sebelumnya pada percobaan ulang, meskipun percobaan ulang biasa tanpa token biasanya menghapusnya. Body harus cocok dengan permintaan yang ditolak, dan server menangani blok-blok tersebut sendiri.
</Accordion>

<Accordion title="Header beta juga harus cocok">
  Kirim header `anthropic-beta` yang sama pada percobaan ulang seperti pada permintaan yang ditolak. Header beta yang ada pada salah satu dari dua permintaan tetapi tidak pada yang lain dapat menggagalkan kecocokan meskipun body-nya identik. Error 400 yang dihasilkan membawa pesan `request body ... does not match` yang sama seperti perbedaan body, sehingga perbedaan header mudah disalahartikan sebagai masalah body. Secara khusus, jangan menambahkan atau menghapus header beta berdasarkan model mana yang ditargetkan oleh permintaan.

  Dua keluarga header dikecualikan dari kecocokan, demi kepentingan percobaan ulang:

  * **`server-side-fallback-*`:** percobaan ulang harus menghapus parameter `fallbacks`, dan menghapus header ini bersamanya tidak menyebabkan ketidakcocokan.
  * **`fallback-credit-*`:** pertahankan header ini pada kedua permintaan. Percobaan ulang memerlukannya untuk menukarkan token.

  <Note>
    Pada model yang menyertakan jendela konteks 1M token secara default, seperti Claude Fable 5 dan Claude Opus 4.8, header beta `context-1m-2025-08-07` tidak memiliki efek. Cara paling andal untuk menjaga kedua permintaan tetap identik adalah dengan menghilangkan header tersebut pada keduanya, daripada mengirimkannya pada satu permintaan dan tidak pada yang lain.
  </Note>
</Accordion>

<Accordion title="Ketika fallback_has_prefill_claim tidak ada">
  Field ini bernilai `null` hanya ketika token juga `null`, sehingga nilai yang Anda amati saat memegang token tidak pernah `null`. Field ini masih dapat muncul sebagai tidak ada (`None` dalam SDK bertipe) pada Amazon Bedrock, Google Cloud, dan Microsoft Foundry sementara dukungan mereka untuk field ini sedang diluncurkan. Dalam kasus itu, perlakukan bentuk percobaan ulang sebagai tidak diketahui, bukan sebagai `false`. Coba bentuk dengan pesan assistant yang ditambahkan terlebih dahulu, dan andalkan penanganan penolakan dalam [Ketika percobaan ulang ditolak](#when-a-retry-is-rejected), yang akan jatuh kembali ke body tanpa perubahan.
</Accordion>

<Accordion title="Menyalin content dari respons yang ditolak">
  Ketika token dari sebuah penolakan mendukung bentuk kelanjutan, `content` respons hanya membawa output model itu sendiri, dan penjelasan penolakan disampaikan dalam `stop_details.explanation`. Oleh karena itu, Anda dapat menyalin `content` ke dalam pesan assistant yang ditambahkan apa adanya.

  Dua penyesuaian mungkin masih diperlukan sebelum mengirim:

  * Jika blok terakhir yang Anda kirim adalah blok `text`, hapus whitespace di akhirnya.
  * Hilangkan blok `tool_use` sisi klien mana pun yang tidak memiliki `tool_result` yang cocok.

  Jika content yang disalin menyertakan blok `fallback` dari [fallback sisi server](/docs/id/build-with-claude/refusals-and-fallback#server-side-fallback) sebelumnya, pertahankan blok tersebut tepat di tempat ia muncul. Blok ini diterima pada permintaan apa pun tanpa header beta. API menggunakan posisinya untuk memvalidasi blok thinking di sekitarnya, sehingga permintaan yang menyalin blok thinking dari kedua sisi batas tersebut akan ditolak jika blok tersebut dihilangkan atau dipindahkan.
</Accordion>

<Accordion title="Cakupan dan masa berlaku token">
  Token hanya dapat ditukarkan dari organisasi dan workspace yang menerima penolakan, termasuk pada Microsoft Foundry. Pada Amazon Bedrock dan Google Cloud, yang tidak memiliki workspace, token terikat pada identitas pemanggil platform sebagai gantinya.

  Token kedaluwarsa lima menit setelah penolakan. Setelah itu, kirim percobaan ulang tanpanya. Token juga bersifat stateless: server tidak menyimpan apa pun tentangnya, dan tidak ada endpoint untuk memeriksa atau mencabutnya.
</Accordion>

<Accordion title="Ketika token tidak dapat ditukarkan oleh kedua bentuk">
  Ketika penolakan tiba setelah alat server telah dieksekusi dalam permintaan, token hanya dapat ditukarkan dengan melanjutkan respons parsial. Pembatasan itulah yang mencegah panggilan alat yang telah selesai dijalankan, dan ditagih, lagi.

  Oleh karena itu, satu kombinasi dapat membuat token tidak dapat ditukarkan oleh kedua bentuk, ketika kedua hal berikut benar:

  * Permintaan menggunakan `output_config.format` atau `tool_choice` yang memaksa penggunaan alat. Salah satunya mengesampingkan bentuk dengan pesan assistant yang ditambahkan.
  * Penolakan tiba setelah alat server telah dieksekusi. Itu mengesampingkan body tanpa perubahan.

  Jika percobaan ulang dengan body tanpa perubahan ditolak dengan error 400 yang menyatakan bahwa token harus ditukarkan dengan melanjutkan respons parsial, buang token tersebut. Percobaan ulang tanpanya akan berhasil diproses, tetapi akan menjalankan ulang dan menagih ulang alat server yang telah selesai. Tampilkan biaya atau error tersebut kepada pemanggil Anda daripada mencoba ulang secara diam-diam.
</Accordion>

## Langkah selanjutnya

<CardGroup>
  <Card title="Penolakan dan fallback" icon="shield" href="/docs/id/build-with-claude/refusals-and-fallback">
    Deteksi penolakan dan pilih antara fallback sisi server, middleware SDK, dan percobaan ulang manual.
  </Card>

  <Card title="Caching prompt" icon="bolt" href="/docs/id/build-with-claude/prompt-caching">
    Bagaimana pembacaan cache dan penulisan cache ditagih.
  </Card>

  <Card title="Stop reason dan fallback" icon="code" href="/docs/id/build-with-claude/handling-stop-reasons">
    Setiap nilai `stop_reason` dan cara menanganinya.
  </Card>

  <Card title="Middleware SDK" icon="settings" href="/docs/id/cli-sdks-libraries/middleware">
    Helper SDK yang menerapkan kredit fallback secara otomatis.
  </Card>
</CardGroup>
