---
source: platform
url: https://platform.claude.com/docs/id/api/sdks/go
fetched_at: 2026-04-18T03:10:04.936408Z
sha256: 2538b384cc633ae548315deae105e3d07d2f7fde2bb5e8426feb8b90d8517eb0
---

# Go SDK

Instal dan konfigurasi Anthropic Go SDK dengan pembatalan berbasis konteks dan opsi fungsional

---

Perpustakaan Anthropic Go menyediakan akses yang nyaman ke Anthropic REST API dari aplikasi yang ditulis dalam Go.

<Info>
Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini mencakup fitur SDK khusus Go dan konfigurasi.
</Info>

## Instalasi

```go nocheck
import (
	"github.com/anthropics/anthropic-sdk-go" // imported as anthropic
)
```

Atau untuk menentukan versi:

```bash
go get -u 'github.com/anthropics/anthropic-sdk-go@v1.27.1'
```

## Persyaratan

Perpustakaan ini memerlukan Go 1.23+.

## Penggunaan

```go nocheck
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
		Model: anthropic.ModelClaudeOpus4_7,
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
	Model:     anthropic.ModelClaudeOpus4_7,
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
	Model:     anthropic.ModelClaudeOpus4_7,
	Messages:  messages,
	MaxTokens: 1024,
})

fmt.Printf("%+v\n", message.Content)
```

</section>
<section title="Prompt sistem">

```go hidelines={1,10..11}
messages := []anthropic.MessageParam{anthropic.NewUserMessage(anthropic.NewTextBlock("Hello"))}
message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
	Model:     anthropic.ModelClaudeOpus4_7,
	MaxTokens: 1024,
	System: []anthropic.TextBlockParam{
		{Text: "Be very serious at all times."},
	},
	Messages: messages,
})
_ = message
_ = err
```

</section>
<section title="Streaming">

```go
content := "What is a quaternion?"

stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
	Model:     anthropic.ModelClaudeOpus4_7,
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

```go hidelines={1..18,99..135}
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
			Model:     anthropic.ModelClaudeOpus4_7,
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
dari rilis `encoding/json` Go 1.24+ untuk bidang permintaan.

Bidang primitif yang diperlukan (`int64`, `string`, dll.) menampilkan tag `` `json:"...,required"` ``. Bidang-bidang ini
selalu diserialisasi, bahkan nilai nolnya.

Tipe primitif opsional dibungkus dalam `param.Opt[T]`. Bidang-bidang ini dapat diatur dengan konstruktor yang disediakan, `anthropic.String(string)`, `anthropic.Int(int64)`, dll.

Setiap `param.Opt[T]`, peta, irisan, struct atau enum string menggunakan
tag `` `json:"...,omitzero"` ``. Nilai nolnya dianggap dihilangkan.

Fungsi `param.IsOmitted(any)` dapat mengonfirmasi kehadiran bidang `omitzero` apa pun.

```go nocheck
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

```go nocheck
p.Name = param.Null[string]()       // 'null' instead of string
p.Point = param.NullStruct[Point]() // 'null' instead of struct

param.IsNull(p.Name)  // true
param.IsNull(p.Point) // true
```

Struct permintaan berisi metode `.SetExtraFields(map[string]any)` yang dapat mengirim
bidang yang tidak sesuai dalam badan permintaan. Bidang tambahan menimpa bidang struct apa pun dengan kunci yang cocok.

<Warning>
Untuk alasan keamanan, hanya gunakan `SetExtraFields` dengan data yang terpercaya.
</Warning>

Untuk mengirim nilai kustom alih-alih struct, gunakan fungsi generik `param.Override` (misalnya, `param.Override[anthropic.FooParams](12)`).

```go nocheck
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
Metode-metode ini mengembalikan pointer yang dapat dimutasi ke data yang mendasar, jika ada.

```go nocheck
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

### Deserialisasi param

<Note>
`param.SetJSON` memerlukan SDK v1.20.0 atau lebih baru.
</Note>

Tipe param (tipe yang berakhir dengan `Param`, seperti `MessageNewParams` atau `ToolUnionParam`) dirancang hanya untuk permintaan keluar. Mereka melakukan marshaling dengan benar ke JSON tetapi tidak sepenuhnya mendukung deserialisasi round-trip. Jika Anda melakukan unmarshal JSON mentah ke dalam struct param, bidang gabungan yang diketik seperti `OfBashTool20250124` akan nil bahkan ketika JSON yang mendasar valid.

Jika Anda perlu merekonstruksi param dari JSON mentah (misalnya, dari database, middleware, atau permintaan sebelumnya), panggil `UnmarshalJSON` untuk mengisi bidang non-gabungan, kemudian gunakan `param.SetJSON` untuk melampirkan byte mentah untuk re-serialisasi yang benar:

```go hidelines={1..24,44}
package main

import (
	"encoding/json"
	"fmt"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/packages/param"
)

func main() {
	original := anthropic.MessageNewParams{
		Model:     anthropic.ModelClaudeOpus4_7,
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{
			anthropic.NewUserMessage(anthropic.NewTextBlock("hello")),
		},
		Tools: []anthropic.ToolUnionParam{{
			OfBashTool20250124: &anthropic.ToolBash20250124Param{
				Type: "bash_20250124",
				Name: "bash",
			},
		}},
	}
	// Serialize params (for example, for storage or forwarding)
	b, err := json.Marshal(original)
	if err != nil {
		panic(err)
	}

	// Later, reconstruct params from the stored JSON
	var params anthropic.MessageNewParams
	if err := params.UnmarshalJSON(b); err != nil {
		panic(err)
	}
	param.SetJSON(b, &params)

	// params.Model and other scalar fields are populated by UnmarshalJSON.
	// params.Tools[0].OfBashTool20250124 is nil (the union limitation),
	// but the raw JSON is preserved. When params is marshaled again
	// for the API call, the tools serialize correctly.
	b2, _ := json.Marshal(params)
	fmt.Println(string(b) == string(b2)) // true
}
```

Untuk kasus penggunaan ini, `param.SetJSON` (tersedia sejak v1.20.0) lebih disukai daripada `param.Override[T](any)` yang lebih umum karena tidak memerlukan pengejaan parameter tipe dan membuat niat round-trip eksplisit.

## Objek respons

Semua bidang dalam struct respons adalah tipe nilai biasa (bukan pointer atau pembungkus).
Struct respons juga menyertakan bidang khusus `JSON` yang berisi metadata tentang
setiap properti.

```go nocheck
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
`.Valid()` mengembalikan true jika bidang bukan `null`, tidak ada, atau tidak dapat di-marshal.

Jika `.Valid()` adalah false, bidang yang sesuai akan menjadi nilai nolnya.

```go nocheck
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

```go nocheck
body := res.JSON.ExtraFields["my_unexpected_field"].Raw()
```

### Gabungan respons

Dalam respons, gabungan direpresentasikan oleh struct yang diratakan yang berisi semua bidang yang mungkin dari setiap
varian objek.
Untuk mengonversinya ke varian, gunakan metode `.AsFooVariant()` atau metode `.AsAny()` jika ada.

Jika nilai gabungan respons berisi nilai primitif, bidang primitif akan bersama
properti tetapi diawali dengan `Of` dan menampilkan tag `json:"...,inline"`.

```go nocheck
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

## Penanganan kesalahan

Ketika API mengembalikan kode status non-sukses, SDK mengembalikan kesalahan dengan tipe
`*anthropic.Error`. Ini berisi nilai `StatusCode`, `*http.Request`, dan
`*http.Response` dari permintaan, serta JSON dari badan kesalahan
(mirip dengan objek respons lainnya dalam SDK). Kesalahan juga menyertakan `RequestID`
dari header respons, yang berguna untuk pemecahan masalah dengan dukungan Anthropic.

Untuk menangani kesalahan, gunakan pola `errors.As`:

```go hidelines={1..11,33}
package main

import (
	"context"
	"errors"

	"github.com/anthropics/anthropic-sdk-go"
)

func main() {
	client := anthropic.NewClient()
	_, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
		MaxTokens: 1024,
		Messages: []anthropic.MessageParam{{
			Content: []anthropic.ContentBlockParamUnion{{
				OfText: &anthropic.TextBlockParam{
					Text: "What is a quaternion?",
				},
			}},
			Role: anthropic.MessageParamRoleUser,
		}},
		Model: anthropic.ModelClaudeOpus4_7,
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
}
```

Ketika kesalahan lain terjadi, mereka dikembalikan tanpa dibungkus; misalnya,
jika transportasi HTTP gagal, Anda mungkin menerima `*url.Error` yang membungkus `*net.OpError`.

## Percobaan ulang

Kesalahan tertentu akan secara otomatis dicoba ulang 2 kali secara default, dengan backoff eksponensial pendek.
SDK mencoba ulang secara default semua kesalahan koneksi, 408 Request Timeout, 409 Conflict, 429 Rate Limit,
dan >=500 kesalahan Internal.

Anda dapat menggunakan opsi `WithMaxRetries` untuk mengonfigurasi atau menonaktifkan ini:

```go hidelines={1..10,17,34}
package main

import (
	"context"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
	// Configure the default for all requests:
	client := anthropic.NewClient(
		option.WithMaxRetries(0), // default is 2
	)

	// Override per-request:
	_, _ =
		client.Messages.New(
			context.TODO(),
			anthropic.MessageNewParams{
				MaxTokens: 1024,
				Messages: []anthropic.MessageParam{{
					Content: []anthropic.ContentBlockParamUnion{{
						OfText: &anthropic.TextBlockParam{
							Text: "What is a quaternion?",
						},
					}},
					Role: anthropic.MessageParamRoleUser,
				}},
				Model: anthropic.ModelClaudeOpus4_7,
			},
			option.WithMaxRetries(5),
		)
}
```

## Batas waktu

Permintaan tidak memiliki batas waktu secara default; gunakan konteks untuk mengonfigurasi batas waktu untuk siklus hidup permintaan.

Perhatikan bahwa jika permintaan [dicoba ulang](#retries), batas waktu konteks tidak dimulai ulang.
Untuk menetapkan batas waktu per-percobaan, gunakan `option.WithRequestTimeout()`.

```go hidelines={1..12,16,34}
package main

import (
	"context"
	"time"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
	client := anthropic.NewClient()
	// This sets the timeout for the request, including all the retries.
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
	defer cancel()
	_, _ =
		client.Messages.New(
			ctx,
			anthropic.MessageNewParams{
				MaxTokens: 1024,
				Messages: []anthropic.MessageParam{{
					Content: []anthropic.ContentBlockParamUnion{{
						OfText: &anthropic.TextBlockParam{
							Text: "What is a quaternion?",
						},
					}},
					Role: anthropic.MessageParamRoleUser,
				}},
				Model: anthropic.ModelClaudeOpus4_7,
			},
			// This sets the per-retry timeout
			option.WithRequestTimeout(20*time.Second),
		)
}
```

## Permintaan panjang

<Warning>
Pertimbangkan menggunakan API Messages streaming untuk permintaan yang berjalan lebih lama.
</Warning>

Hindari menetapkan nilai `MaxTokens` yang besar tanpa menggunakan streaming karena beberapa jaringan mungkin memutuskan koneksi idle setelah periode waktu tertentu, yang
dapat menyebabkan permintaan gagal atau [timeout](#timeouts) tanpa menerima respons dari Anthropic.

SDK ini juga akan mengembalikan kesalahan jika permintaan non-streaming diharapkan melebihi kira-kira 10 menit.
Memanggil `.Messages.NewStreaming()` atau [menetapkan batas waktu kustom](#timeouts) menonaktifkan kesalahan ini.

## Unggahan file

Parameter permintaan yang sesuai dengan unggahan file dalam permintaan multipart diketik sebagai
`io.Reader`. Konten `io.Reader` akan secara default dikirim sebagai bagian formulir multipart
dengan nama file "anonymous_file" dan content-type "application/octet-stream", jadi pendekatan yang direkomendasikan adalah menentukan content-type kustom dengan pembantu `anthropic.File(reader io.Reader, filename string, contentType string)`
, yang dengan mudah membungkus `io.Reader` apa pun dengan nama file dan tipe konten yang sesuai.

```go nocheck
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

Nama file dan content-type juga dapat disesuaikan dengan mengimplementasikan `Name() string` atau `ContentType()
string` pada tipe runtime `io.Reader`. Perhatikan bahwa `os.File` mengimplementasikan `Name() string`, jadi file yang dikembalikan oleh `os.Open` akan dikirim dengan nama file di disk.

## Paginasi

Perpustakaan ini menyediakan beberapa kemudahan untuk bekerja dengan endpoint daftar yang dipaginasi.

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
paket `option` mengembalikan `RequestOption`, yang merupakan closure yang
mengubah `RequestConfig`. Opsi-opsi ini dapat disediakan ke klien atau pada permintaan individual.
Misalnya:

```go nocheck
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

SDK menyediakan `option.WithMiddleware`, yang menerapkan middleware yang diberikan
ke permintaan.

```go hidelines={1..16,32..33}
package main

import (
	"net/http"
	"time"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
)

var _ = anthropic.ModelClaudeOpus4_7

func LogReq(req *http.Request)                              {}
func LogRes(res *http.Response, err error, d time.Duration) {}

func main() {
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
	_ = client
}
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
Untuk panduan penyiapan platform terperinci dengan contoh kode, lihat:
- [Amazon Bedrock](/docs/id/build-with-claude/claude-on-amazon-bedrock)
- [Google Vertex AI](/docs/id/build-with-claude/claude-on-vertex-ai)
</Note>

Go SDK mendukung Amazon Bedrock dan Google Vertex AI melalui subpaket:

- **Bedrock:** `import "github.com/anthropics/anthropic-sdk-go/bedrock"`. Gunakan `bedrock.WithLoadDefaultConfig(ctx)` atau `bedrock.WithConfig(cfg)`. Mengimpor paket ini secara global mendaftarkan decoder untuk `application/vnd.amazon.eventstream` untuk streaming.
- **Vertex AI:** `import "github.com/anthropics/anthropic-sdk-go/vertex"`. Gunakan `vertex.WithGoogleAuth(ctx, region, projectID)` atau `vertex.WithCredentials(ctx, region, projectID, creds)`.

## Penggunaan lanjutan

### Mengakses data respons mentah (misalnya, header respons)

Anda dapat mengakses data respons HTTP mentah dengan menggunakan opsi permintaan `option.WithResponseInto()`. Ini berguna ketika
Anda perlu memeriksa header respons, kode status, atau detail lainnya.

```go hidelines={1..13,39}
package main

import (
	"context"
	"fmt"
	"net/http"

	"github.com/anthropics/anthropic-sdk-go"
	"github.com/anthropics/anthropic-sdk-go/option"
)

func main() {
	client := anthropic.NewClient()
	// Create a variable to store the HTTP response
	var response *http.Response
	message, err := client.Messages.New(
		context.TODO(),
		anthropic.MessageNewParams{
			MaxTokens: 1024,
			Messages: []anthropic.MessageParam{{
				Content: []anthropic.ContentBlockParamUnion{{
					OfText: &anthropic.TextBlockParam{
						Text: "What is a quaternion?",
					},
				}},
				Role: anthropic.MessageParamRoleUser,
			}},
			Model: anthropic.ModelClaudeOpus4_7,
		},
		option.WithResponseInto(&response),
	)
	if err != nil {
		// handle error
	}
	fmt.Printf("%+v\n", message)

	fmt.Printf("Status Code: %d\n", response.StatusCode)
	fmt.Printf("Headers: %+#v\n", response.Header)
}
```

### Membuat permintaan kustom/tidak terdokumentasi

Perpustakaan ini diketik untuk akses yang nyaman ke API yang terdokumentasi. Jika Anda perlu mengakses endpoint,
param, atau properti respons yang tidak terdokumentasi, perpustakaan masih dapat digunakan.

#### Endpoint yang tidak terdokumentasi

Untuk membuat permintaan ke endpoint yang tidak terdokumentasi, Anda dapat menggunakan `client.Get`, `client.Post`, dan verba HTTP lainnya.
`RequestOptions` pada klien, seperti percobaan ulang, akan dihormati saat membuat permintaan ini.

```go nocheck
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

Untuk membuat permintaan menggunakan parameter yang tidak terdokumentasi, Anda dapat menggunakan metode `option.WithQuerySet()`
atau metode `option.WithJSONSet()`.

```go nocheck
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
dengan `result.JSON.RawJSON()`, atau mendapatkan JSON mentah bidang tertentu pada hasil dengan
`result.JSON.Foo.Raw()`.

Bidang apa pun yang tidak ada pada struct respons akan disimpan dan dapat diakses oleh `result.JSON.ExtraFields()` yang mengembalikan bidang tambahan sebagai `map[string]Field`.

## Versioning semantik

Paket ini umumnya mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html), meskipun perubahan yang tidak kompatibel ke belakang tertentu dapat dirilis sebagai versi minor:

1. Perubahan pada internal perpustakaan yang secara teknis publik tetapi tidak dimaksudkan atau didokumentasikan untuk penggunaan eksternal. _(Silakan buka masalah GitHub untuk memberi tahu pemelihara jika Anda mengandalkan internal tersebut.)_
2. Perubahan yang tidak diharapkan berdampak pada sebagian besar pengguna dalam praktik.

Kompatibilitas ke belakang ditanggapi dengan serius untuk memastikan Anda dapat mengandalkan pengalaman upgrade yang lancar.

Umpan balik Anda disambut; silakan buka [masalah](https://www.github.com/anthropics/anthropic-sdk-go/issues) dengan pertanyaan, bug, atau saran.

## Sumber daya tambahan

- [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-go)
- [Dokumentasi paket Go](https://pkg.go.dev/github.com/anthropics/anthropic-sdk-go)
- [Referensi API](/docs/id/api/overview)
- [Panduan streaming](/docs/id/build-with-claude/streaming)