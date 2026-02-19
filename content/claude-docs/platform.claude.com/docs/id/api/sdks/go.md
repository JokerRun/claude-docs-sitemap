---
source: platform
url: https://platform.claude.com/docs/id/api/sdks/go
fetched_at: 2026-02-19T04:23:04.153807Z
sha256: 18f1969eb0e83c2fe9a7dd365ea1f34f958c61c732022a2a6159f648c35ebd23
---

# Go SDK

Instal dan konfigurasi Anthropic Go SDK dengan pembatalan berbasis konteks dan opsi fungsional

---

Perpustakaan Anthropic Go menyediakan akses yang mudah ke Anthropic REST API dari aplikasi yang ditulis dalam Go.

<Info>
Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini mencakup fitur SDK khusus Go dan konfigurasi.
</Info>

## Instalasi

```go
import (
	"github.com/anthropics/anthropic-sdk-go" // imported as anthropic
)
```

Atau untuk menentukan versi:

```bash
go get -u 'github.com/anthropics/anthropic-sdk-go@v1.19.0'
```

## Persyaratan

Perpustakaan ini memerlukan Go 1.22+.

## Penggunaan

```go
package main

import (
	"context"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
	client := anthropic.NewClient(
		option.WithAPIKey("my-anthropic-api-key"), // defaults to os.LookupEnv("ANTHROPIC_API_KEY")
	)
	message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("What is a quaternion?")),
		},
		Model: anthropic.ModelClaudeOpus4_6,
	})
	if err != nil {
		panic(err.Error())
	}
	fmt.Printf("%+v\n", message.Content)
}
```

<section title="Percakapan">

```go
messages := []anthropic.MessageParam{
	anthropic.NewUserMessage(anthropic.NewTextBlock("What is my first name?")),
}

message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
	Model:     anthropic.ModelClaudeOpus4_6,
	Messages:  messages,
	MaxTokens: 1024,
})
if err != nil {
	panic(err)
}

fmt.Printf("%+v\n", message.Content)

messages = append(messages, message.ToParam())
messages = append(messages, anthropic.NewUserMessage(
	anthropic.NewTextBlock("My full name is John Doe"),
))

message, err = client.Messages.New(context.TODO(), anthropic.MessageNewParams{
	Model:     anthropic.ModelClaudeOpus4_6,
	Messages:  messages,
	MaxTokens: 1024,
})

fmt.Printf("%+v\n", message.Content)
```

</section>
<section title="Prompt sistem">

```go
message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
	Model:     anthropic.ModelClaudeOpus4_6,
	MaxTokens: 1024,
	System: []anthropic.TextBlockParam{
		{Text: "Be very serious at all times."},
	},
	Messages: messages,
})
```

</section>
<section title="Streaming">

```go
content := "What is a quaternion?"

stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
	Model:     anthropic.ModelClaudeOpus4_6,
	MaxTokens: 1024,
	Messages: []anthropic.MessageParam{
		anthropic.NewUserMessage(anthropic.NewTextBlock(content)),
	},
})

message := anthropic.Message{}
for stream.Next() {
	event := stream.Current()
	err := message.Accumulate(event)
	if err != nil {
		panic(err)
	}

	switch eventVariant := event.AsAny().(type) {
	case anthropic.ContentBlockDeltaEvent:
		switch deltaVariant := eventVariant.Delta.AsAny().(type) {
		case anthropic.TextDelta:
			print(deltaVariant.Text)
		}

	}
}

if stream.Err() != nil {
	panic(stream.Err())
}
```

</section>
<section title="Pemanggilan alat">

```go
package main

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/invopop/jsonschema"
)

func main() {
	client := anthropic.NewClient()

	content := "Where is San Francisco?"

	println("[user]: " + content)

	messages := []anthropic.MessageParam{
		anthropic.NewUserMessage(anthropic.NewTextBlock(content)),
	}

	toolParams := []anthropic.ToolParam{
		{
			Name:        "get_coordinates",
			Description: anthropic.String("Accepts a place as an address, then returns the latitude and longitude coordinates."),
			InputSchema: GetCoordinatesInputSchema,
		},
	}
	tools := make([]anthropic.ToolUnionParam, len(toolParams))
	for i, toolParam := range toolParams {
		tools[i] = anthropic.ToolUnionParam{OfTool: &toolParam}
	}

	for {
		message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
			Model:     anthropic.ModelClaudeOpus4_6,
			MaxTokens: 1024,
			Messages:  messages,
			Tools:     tools,
		})

		if err != nil {
			panic(err)
		}

		print(color("[assistant]: "))
		for _, block := range message.Content {
			switch block := block.AsAny().(type) {
			case anthropic.TextBlock:
				println(block.Text)
				println()
			case anthropic.ToolUseBlock:
				inputJSON, _ := json.Marshal(block.Input)
				println(block.Name + ": " + string(inputJSON))
				println()
			}
		}

		messages = append(messages, message.ToParam())
		toolResults := []anthropic.ContentBlockParamUnion{}

		for _, block := range message.Content {
			switch variant := block.AsAny().(type) {
			case anthropic.ToolUseBlock:
				print(color("[user (" + block.Name + ")]: "))

				var response interface{}
				switch block.Name {
				case "get_coordinates":
					var input struct {
						Location string `json:"location"`
					}

					err := json.Unmarshal([]byte(variant.JSON.Input.Raw()), &input)
					if err != nil {
						panic(err)
					}

					response = GetCoordinates(input.Location)
				}

				b, err := json.Marshal(response)
				if err != nil {
					panic(err)
				}

				println(string(b))

				toolResults = append(toolResults, anthropic.NewToolResultBlock(block.ID, string(b), false))
			}

		}
		if len(toolResults) == 0 {
			break
		}
		messages = append(messages, anthropic.NewUserMessage(toolResults...))
	}
}

type GetCoordinatesInput struct {
	Location string `json:"location" jsonschema_description:"The location to look up."`
}

var GetCoordinatesInputSchema = GenerateSchema[GetCoordinatesInput]()

type GetCoordinateResponse struct {
	Long float64 `json:"long"`
	Lat  float64 `json:"lat"`
}

func GetCoordinates(location string) GetCoordinateResponse {
	return GetCoordinateResponse{
		Long: -122.4194,
		Lat:  37.7749,
	}
}

func GenerateSchema[T any]() anthropic.ToolInputSchemaParam {
	reflector := jsonschema.Reflector{
		AllowAdditionalProperties: false,
		DoNotReference:            true,
	}
	var v T

	schema := reflector.Reflect(v)

	return anthropic.ToolInputSchemaParam{
		Properties: schema.Properties,
	}
}

func color(s string) string {
	return fmt.Sprintf("\033[1;%sm%s\033[0m", "33", s)
}
```

</section>

## Bidang permintaan

Perpustakaan anthropic menggunakan semantik [`omitzero`](https://tip.golang.org/doc/go1.24#encodingjsonpkgencodingjson)
dari rilis Go 1.24+ `encoding/json` untuk bidang permintaan.

Bidang primitif yang diperlukan (`int64`, `string`, dll.) menampilkan tag `` `json:"...,required"` ``. Bidang-bidang ini
selalu diserialisasi, bahkan nilai nolnya.

Tipe primitif opsional dibungkus dalam `param.Opt[T]`. Bidang-bidang ini dapat diatur dengan konstruktor yang disediakan, `anthropic.String(string)`, `anthropic.Int(int64)`, dll.

Setiap `param.Opt[T]`, peta, irisan, struct atau enum string menggunakan
tag `` `json:"...,omitzero"` ``. Nilai nolnya dianggap dihilangkan.

Fungsi `param.IsOmitted(any)` dapat mengkonfirmasi kehadiran bidang `omitzero` apa pun.

```go
p := anthropic.ExampleParams{
	ID:   "id_xxx",                // required property
	Name: anthropic.String("..."), // optional property

	Point: anthropic.Point{
		X: 0,                // required field will serialize as 0
		Y: anthropic.Int(1), // optional field will serialize as 1
		// ... omitted non-required fields will not be serialized
	},

	Origin: anthropic.Origin{}, // the zero value of [Origin] is considered omitted
}
```

Untuk mengirim `null` alih-alih `param.Opt[T]`, gunakan `param.Null[T]()`.
Untuk mengirim `null` alih-alih struct `T`, gunakan `param.NullStruct[T]()`.

```go
p.Name = param.Null[string]()       // 'null' instead of string
p.Point = param.NullStruct[Point]() // 'null' instead of struct

param.IsNull(p.Name)  // true
param.IsNull(p.Point) // true
```

Struct permintaan berisi metode `.SetExtraFields(map[string]any)` yang dapat mengirim
bidang yang tidak sesuai dalam badan permintaan. Bidang tambahan menimpa bidang struct apa pun dengan kunci yang cocok.

<Warning>
Untuk alasan keamanan, hanya gunakan `SetExtraFields` dengan data terpercaya.
</Warning>

Untuk mengirim nilai kustom alih-alih struct, gunakan `param.Override[T](value)`.

```go
// In cases where the API specifies a given type,
// but you want to send something else, use [SetExtraFields]:
p.SetExtraFields(map[string]any{
	"x": 0.01, // send "x" as a float instead of int
})

// Send a number instead of an object
custom := param.Override[anthropic.FooParams](12)
```

### Gabungan permintaan

Gabungan direpresentasikan sebagai struct dengan bidang yang diawali dengan "Of" untuk setiap variannya,
hanya satu bidang yang dapat bukan nol. Bidang bukan nol akan diserialisasi.

Sub-properti gabungan dapat diakses melalui metode pada struct gabungan.
Metode-metode ini mengembalikan pointer yang dapat dimutasi ke data yang mendasarinya, jika ada.

```go
// Only one field can be non-zero, use param.IsOmitted() to check if a field is set
type AnimalUnionParam struct {
	OfCat *Cat `json:",omitzero,inline`
	OfDog *Dog `json:",omitzero,inline`
}

animal := AnimalUnionParam{
	OfCat: &Cat{
		Name: "Whiskers",
		Owner: PersonParam{
			Address: AddressParam{Street: "3333 Coyote Hill Rd", Zip: 0},
		},
	},
}

// Mutating a field
if address := animal.GetOwner().GetAddress(); address != nil {
	address.ZipCode = 94304
}
```

## Objek respons

Semua bidang dalam struct respons adalah tipe nilai biasa (bukan pointer atau pembungkus).
Struct respons juga menyertakan bidang khusus `JSON` yang berisi metadata tentang
setiap properti.

```go
type Animal struct {
	Name   string `json:"name,nullable"`
	Owners int    `json:"owners"`
	Age    int    `json:"age"`
	JSON   struct {
		Name        respjson.Field
		Owner       respjson.Field
		Age         respjson.Field
		ExtraFields map[string]respjson.Field
	} `json:"-"`
}
```

Untuk menangani data opsional, gunakan metode `.Valid()` pada bidang JSON.
`.Valid()` mengembalikan true jika bidang bukan `null`, tidak ada, atau tidak dapat diserialisasi.

Jika `.Valid()` adalah false, bidang yang sesuai akan menjadi nilai nolnya.

```go
raw := `{"owners": 1, "name": null}`

var res Animal
json.Unmarshal([]byte(raw), &res)

// Accessing regular fields

res.Owners // 1
res.Name   // ""
res.Age    // 0

// Optional field checks

res.JSON.Owners.Valid() // true
res.JSON.Name.Valid()   // false
res.JSON.Age.Valid()    // false

// Raw JSON values

res.JSON.Owners.Raw()                  // "1"
res.JSON.Name.Raw() == "null"          // true
res.JSON.Name.Raw() == respjson.Null   // true
res.JSON.Age.Raw() == ""               // true
res.JSON.Age.Raw() == respjson.Omitted // true
```

Struct `.JSON` ini juga menyertakan peta `ExtraFields` yang berisi
properti apa pun dalam respons json yang tidak ditentukan
dalam struct. Ini dapat berguna untuk fitur API yang belum ada
dalam SDK.

```go
body := res.JSON.ExtraFields["my_unexpected_field"].Raw()
```

### Gabungan respons

Dalam respons, gabungan direpresentasikan oleh struct yang diratakan yang berisi semua bidang yang mungkin dari setiap
varian objek.
Untuk mengonversinya ke varian, gunakan metode `.AsFooVariant()` atau metode `.AsAny()` jika ada.

Jika gabungan nilai respons berisi nilai primitif, bidang primitif akan bersama
properti tetapi diawali dengan `Of` dan menampilkan tag `json:"...,inline"`.

```go
type AnimalUnion struct {
	// From variants [Dog], [Cat]
	Owner Person `json:"owner"`
	// From variant [Dog]
	DogBreed string `json:"dog_breed"`
	// From variant [Cat]
	CatBreed string `json:"cat_breed"`
	// ...

	JSON struct {
		Owner respjson.Field
		// ...
	} `json:"-"`
}

// If animal variant
if animal.Owner.Address.ZipCode == "" {
	panic("missing zip code")
}

// Switch on the variant
switch variant := animal.AsAny().(type) {
case Dog:
case Cat:
default:
	panic("unexpected type")
}
```

## Streaming

Gunakan API streaming untuk respons real-time:

```go
stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
	Model:     anthropic.ModelClaudeOpus4_6,
	MaxTokens: 1024,
	Messages: []anthropic.MessageParam{
		anthropic.NewUserMessage(anthropic.NewTextBlock("What is a quaternion?")),
	},
})

message := anthropic.Message{}
for stream.Next() {
	event := stream.Current()
	err := message.Accumulate(event)
	if err != nil {
		panic(err)
	}

	switch eventVariant := event.AsAny().(type) {
	case anthropic.ContentBlockDeltaEvent:
		switch deltaVariant := eventVariant.Delta.AsAny().(type) {
		case anthropic.TextDelta:
			print(deltaVariant.Text)
		}

	}
}

if stream.Err() != nil {
	panic(stream.Err())
}
```

## Penanganan kesalahan

Ketika API mengembalikan kode status non-sukses, kami mengembalikan kesalahan dengan tipe
`*anthropic.Error`. Ini berisi nilai `StatusCode`, `*http.Request`, dan
`*http.Response` dari permintaan, serta JSON dari badan kesalahan
(mirip dengan objek respons lainnya dalam SDK). Kesalahan juga menyertakan `RequestID`
dari header respons, yang berguna untuk pemecahan masalah dengan dukungan Anthropic.

Untuk menangani kesalahan, kami merekomendasikan agar Anda menggunakan pola `errors.As`:

```go
_, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
	MaxTokens: 1024,
	Messages: []anthropic.MessageParam{{
		Content: []anthropic.ContentBlockParamUnion{{
			OfText: &anthropic.TextBlockParam{Text: "What is a quaternion?", CacheControl: anthropic.CacheControlEphemeralParam{TTL: anthropic.CacheControlEphemeralTTLTTL5m}, Citations: []anthropic.TextCitationParamUnion{{
				OfCharLocation: &anthropic.CitationCharLocationParam{CitedText: "cited_text", DocumentIndex: 0, DocumentTitle: anthropic.String("x"), EndCharIndex: 0, StartCharIndex: 0},
			}}},
		}},
		Role: anthropic.MessageParamRoleUser,
	}},
	Model: anthropic.ModelClaudeOpus4_6,
})
if err != nil {
	var apierr *anthropic.Error
	if errors.As(err, &apierr) {
		println("Request ID:", apierr.RequestID)
		println(string(apierr.DumpRequest(true)))  // Prints the serialized HTTP request
		println(string(apierr.DumpResponse(true))) // Prints the serialized HTTP response
	}
	panic(err.Error()) // GET "/v1/messages": 400 Bad Request (Request-ID: req_xxx) { ... }
}
```

Ketika kesalahan lain terjadi, mereka dikembalikan tanpa dibungkus; misalnya,
jika transportasi HTTP gagal, Anda mungkin menerima `*url.Error` yang membungkus `*net.OpError`.

## Percobaan ulang

Kesalahan tertentu akan secara otomatis dicoba ulang 2 kali secara default, dengan backoff eksponensial pendek.
Kami mencoba ulang secara default semua kesalahan koneksi, 408 Request Timeout, 409 Conflict, 429 Rate Limit,
dan >=500 kesalahan Internal.

Anda dapat menggunakan opsi `WithMaxRetries` untuk mengonfigurasi atau menonaktifkan ini:

```go
// Configure the default for all requests:
client := anthropic.NewClient(
	option.WithMaxRetries(0), // default is 2
)

// Override per-request:
client.Messages.New(
	context.TODO(),
	anthropic.MessageNewParams{
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{{
			Content: []anthropic.ContentBlockParamUnion{{
				OfRequestTextBlock: &anthropic.TextBlockParam{Text: "What is a quaternion?"},
			}},
			Role: anthropic.MessageParamRoleUser,
		}},
		Model: anthropic.ModelClaudeOpus4_6,
	},
	option.WithMaxRetries(5),
)
```

## Batas waktu

Permintaan tidak habis waktu secara default; gunakan konteks untuk mengonfigurasi batas waktu untuk siklus hidup permintaan.

Perhatikan bahwa jika permintaan [dicoba ulang](#retries), batas waktu konteks tidak dimulai ulang.
Untuk mengatur batas waktu per-percobaan, gunakan `option.WithRequestTimeout()`.

```go
// This sets the timeout for the request, including all the retries.
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
defer cancel()
client.Messages.New(
	ctx,
	anthropic.MessageNewParams{
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{{
			Content: []anthropic.ContentBlockParamUnion{{
				OfRequestTextBlock: &anthropic.TextBlockParam{Text: "What is a quaternion?"},
			}},
			Role: anthropic.MessageParamRoleUser,
		}},
		Model: anthropic.ModelClaudeOpus4_6,
	},
	// This sets the per-retry timeout
	option.WithRequestTimeout(20*time.Second),
)
```

## Permintaan panjang

<Warning>
Kami sangat mendorong Anda menggunakan API Messages streaming untuk permintaan yang berjalan lebih lama.
</Warning>

Kami tidak merekomendasikan menetapkan nilai `MaxTokens` besar tanpa menggunakan streaming karena beberapa jaringan mungkin menghapus koneksi idle setelah periode waktu tertentu, yang
dapat menyebabkan permintaan gagal atau [habis waktu](#timeouts) tanpa menerima respons dari Anthropic.

SDK ini juga akan mengembalikan kesalahan jika permintaan non-streaming diharapkan lebih dari kira-kira 10 menit.
Memanggil `.Messages.NewStreaming()` atau [menetapkan batas waktu kustom](#timeouts) menonaktifkan kesalahan ini.

## Unggahan file

Parameter permintaan yang sesuai dengan unggahan file dalam permintaan multipart diketik sebagai
`io.Reader`. Isi `io.Reader` akan secara default dikirim sebagai bagian formulir multipart
dengan nama file "anonymous_file" dan tipe konten "application/octet-stream", jadi kami
merekomendasikan selalu menentukan tipe konten kustom dengan pembantu `anthropic.File(reader io.Reader, filename string, contentType string)`
yang kami sediakan untuk membungkus `io.Reader` dengan mudah dengan nama file dan tipe konten yang sesuai.

```go
// A file from the file system
file, err := os.Open("/path/to/file.json")
anthropic.BetaFileUploadParams{
	File:  anthropic.File(file, "custom-name.json", "application/json"),
	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
}

// A file from a string
anthropic.BetaFileUploadParams{
	File:  anthropic.File(strings.NewReader("my file contents"), "custom-name.json", "application/json"),
	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFilesAPI2025_04_14},
}
```

Nama file dan tipe konten juga dapat disesuaikan dengan mengimplementasikan `Name() string` atau `ContentType()
string` pada tipe runtime `io.Reader`. Perhatikan bahwa `os.File` mengimplementasikan `Name() string`, jadi file yang dikembalikan oleh `os.Open` akan dikirim dengan nama file di disk.

## Paginasi

Perpustakaan ini menyediakan beberapa kemudahan untuk bekerja dengan titik akhir daftar yang dipaginasi.

Anda dapat menggunakan metode `.ListAutoPaging()` untuk mengulangi item di semua halaman:

```go
iter := client.Messages.Batches.ListAutoPaging(context.TODO(), anthropic.MessageBatchListParams{
	Limit: anthropic.Int(20),
})
// Automatically fetches more pages as needed.
for iter.Next() {
	messageBatch := iter.Current()
	fmt.Printf("%+v\n", messageBatch)
}
if err := iter.Err(); err != nil {
	panic(err.Error())
}
```

Atau Anda dapat menggunakan metode `.List()` sederhana untuk mengambil satu halaman dan menerima objek respons standar
dengan metode pembantu tambahan seperti `.GetNextPage()`:

```go
page, err := client.Messages.Batches.List(context.TODO(), anthropic.MessageBatchListParams{
	Limit: anthropic.Int(20),
})
for page != nil {
	for _, batch := range page.Data {
		fmt.Printf("%+v\n", batch)
	}
	page, err = page.GetNextPage()
}
if err != nil {
	panic(err.Error())
}
```

## RequestOptions

Perpustakaan ini menggunakan pola opsi fungsional. Fungsi yang ditentukan dalam
paket `option` mengembalikan `RequestOption`, yang merupakan penutupan yang memutasi
`RequestConfig`. Opsi-opsi ini dapat disuplai ke klien atau pada permintaan individual.
Misalnya:

```go
client := anthropic.NewClient(
	// Adds a header to every request made by the client
	option.WithHeader("X-Some-Header", "custom_header_info"),
)

client.Messages.New(context.TODO(), // ...,
	// Override the header
	option.WithHeader("X-Some-Header", "some_other_custom_header_info"),
	// Add an undocumented field to the request body, using sjson syntax
	option.WithJSONSet("some.json.path", map[string]string{"my": "object"}),
)
```

Opsi permintaan `option.WithDebugLog(nil)` mungkin membantu saat debugging.

Lihat [daftar lengkap opsi permintaan](https://pkg.go.dev/github.com/anthropics/anthropic-sdk-go/option).

## Kustomisasi klien HTTP

### Middleware

Kami menyediakan `option.WithMiddleware` yang menerapkan middleware yang diberikan
ke permintaan.

```go
client := anthropic.NewClient(
	option.WithMiddleware(func(req *http.Request, next option.MiddlewareNext) (res *http.Response, err error) {
		// Before the request
		start := time.Now()
		LogReq(req)

		// Forward the request to the next handler
		res, err = next(req)

		// Handle stuff after the request
		LogRes(res, err, time.Since(start))

		return res, err
	}),
)
```

Ketika beberapa middleware disediakan sebagai argumen variadic, middleware
diterapkan dari kiri ke kanan. Jika `option.WithMiddleware` diberikan
beberapa kali, misalnya pertama di klien kemudian metode, middleware
di klien akan berjalan terlebih dahulu dan middleware yang diberikan dalam metode
akan berjalan berikutnya.

Anda juga dapat mengganti `http.Client` default dengan
`option.WithHTTPClient(client)`. Hanya satu klien http yang
diterima (ini menimpa klien sebelumnya) dan menerima permintaan setelah
middleware apa pun telah diterapkan.

## Integrasi platform

<Note>
Untuk panduan penyiapan platform terperinci, lihat:
- [Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock)
- [Google Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai)
</Note>

### Amazon Bedrock

Untuk menggunakan perpustakaan ini dengan [Amazon Bedrock](https://aws.amazon.com/bedrock/claude/),
gunakan opsi permintaan bedrock `bedrock.WithLoadDefaultConfig(...)` yang membaca
[konfigurasi default](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html).

Mengimpor perpustakaan `bedrock` juga secara global mendaftarkan decoder untuk `application/vnd.amazon.eventstream` untuk
streaming.

```go
package main

import (
	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/bedrock"
)

func main() {
	client := anthropic.NewClient(
		bedrock.WithLoadDefaultConfig(context.Background()),
	)
}
```

Jika Anda sudah memiliki `aws.Config`, Anda juga dapat menggunakannya secara langsung dengan `bedrock.WithConfig(cfg)`.

Baca lebih lanjut tentang Anthropic dan Amazon Bedrock di [Claude on Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock).

### Google Vertex AI

Untuk menggunakan perpustakaan ini dengan [Google Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude),
gunakan opsi permintaan `vertex.WithGoogleAuth(...)` yang membaca
[Application Default Credentials](https://cloud.google.com/docs/authentication/application-default-credentials).

```go
package main

import (
	"context"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/vertex"
)

func main() {
	client := anthropic.NewClient(
		vertex.WithGoogleAuth(context.Background(), "us-central1", "id-xxx"),
	)
}
```

Jika Anda sudah memiliki `*google.Credentials`, Anda juga dapat menggunakannya secara langsung dengan
`vertex.WithCredentials(ctx, region, projectId, creds)`.

Baca lebih lanjut tentang Anthropic dan Google Vertex AI di [Claude on Google Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai).

## Penggunaan lanjutan

### Mengakses data respons mentah (misalnya header respons)

Anda dapat mengakses data respons HTTP mentah dengan menggunakan opsi permintaan `option.WithResponseInto()`. Ini berguna ketika
Anda perlu memeriksa header respons, kode status, atau detail lainnya.

```go
// Create a variable to store the HTTP response
var response *http.Response
message, err := client.Messages.New(
	context.TODO(),
	anthropic.MessageNewParams{
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{{
			Content: []anthropic.ContentBlockParamUnion{{
				OfText: &anthropic.TextBlockParam{Text: "What is a quaternion?", CacheControl: anthropic.CacheControlEphemeralParam{TTL: anthropic.CacheControlEphemeralTTLTTL5m}, Citations: []anthropic.TextCitationParamUnion{{
					OfCharLocation: &anthropic.CitationCharLocationParam{CitedText: "cited_text", DocumentIndex: 0, DocumentTitle: anthropic.String("x"), EndCharIndex: 0, StartCharIndex: 0},
				}}},
			}},
			Role: anthropic.MessageParamRoleUser,
		}},
		Model: anthropic.ModelClaudeOpus4_6,
	},
	option.WithResponseInto(&response),
)
if err != nil {
	// handle error
}
fmt.Printf("%+v\n", message)

fmt.Printf("Status Code: %d\n", response.StatusCode)
fmt.Printf("Headers: %+#v\n", response.Header)
```

### Membuat permintaan kustom/tidak terdokumentasi

Perpustakaan ini diketik untuk akses yang mudah ke API yang terdokumentasi. Jika Anda perlu mengakses titik akhir yang tidak terdokumentasi,
parameter, atau properti respons, perpustakaan masih dapat digunakan.

#### Titik akhir yang tidak terdokumentasi

Untuk membuat permintaan ke titik akhir yang tidak terdokumentasi, Anda dapat menggunakan `client.Get`, `client.Post`, dan verba HTTP lainnya.
`RequestOptions` pada klien, seperti percobaan ulang, akan dihormati saat membuat permintaan ini.

```go
var (
	// params can be an io.Reader, a []byte, an encoding/json serializable object,
	// or a "...Params" struct defined in this library.
	params map[string]any

	// result can be an []byte, *http.Response, a encoding/json deserializable object,
	// or a model defined in this library.
	result *http.Response
)
err := client.Post(context.Background(), "/unspecified", params, &result)
if err != nil {
	// ...
}
```

#### Parameter permintaan yang tidak terdokumentasi

Untuk membuat permintaan menggunakan parameter yang tidak terdokumentasi, Anda dapat menggunakan
`option.WithQuerySet()` atau metode `option.WithJSONSet()`.

```go
params := FooNewParams{
	ID: "id_xxxx",
	Data: FooNewParamsData{
		FirstName: anthropic.String("John"),
	},
}
client.Foo.New(context.Background(), params, option.WithJSONSet("data.last_name", "Doe"))
```

#### Properti respons yang tidak terdokumentasi

Untuk mengakses properti respons yang tidak terdokumentasi, Anda dapat mengakses JSON mentah respons sebagai string
dengan `result.JSON.RawJSON()`, atau mendapatkan JSON mentah dari bidang tertentu pada hasil dengan
`result.JSON.Foo.Raw()`.

Bidang apa pun yang tidak ada pada struct respons akan disimpan dan dapat diakses oleh `result.JSON.ExtraFields()` yang mengembalikan bidang tambahan sebagai `map[string]Field`.

## Sumber daya tambahan

- [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-go)
- [Dokumentasi paket Go](https://pkg.go.dev/github.com/anthropics/anthropic-sdk-go)
- [Referensi API](/docs/id/api/overview)
- [Panduan streaming](/docs/id/build-with-claude/streaming)