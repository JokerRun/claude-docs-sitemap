---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/go
fetched_at: 2026-07-21T03:08:36.086694Z
sha256: 84f6cb1ad22e8d567227f91cef34af1566bb8a516379c85a6a7f0c5f90a7c1fd
---

# Go SDK

Instal dan konfigurasikan Anthropic Go SDK dengan pembatalan berbasis konteks dan opsi fungsional

---

Pustaka Anthropic Go menyediakan akses yang mudah ke Anthropic REST API dari aplikasi yang ditulis dalam Go.

<Info>
  Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](/docs/id/api/overview). Halaman ini membahas fitur dan konfigurasi SDK yang spesifik untuk Go.
</Info>

## Instalasi

```go
import (
	"github.com/anthropics/anthropic-sdk-go" // imported as anthropic
)
```

Instal dengan `go get`:

```bash
go get github.com/anthropics/anthropic-sdk-go
```

## Persyaratan

Pustaka ini memerlukan Go 1.23+.

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
		Model: anthropic.ModelClaudeOpus4_8,
	})
	if err != nil {
		panic(err.Error())
	}
	for _, block := range message.Content {
		if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
			fmt.Println(textBlock.Text)
		}
	}
}
```

Untuk opsi autentikasi termasuk Workload Identity Federation, lihat [Autentikasi](/docs/id/manage-claude/authentication).

<AccordionGroup>
  <Accordion title="Percakapan">
    ```go
    messages := []anthropic.MessageParam{
    	anthropic.NewUserMessage(anthropic.NewTextBlock("What is my first name?")),
    }

    message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    	Model:     anthropic.ModelClaudeOpus4_8,
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
    	Model:     anthropic.ModelClaudeOpus4_8,
    	Messages:  messages,
    	MaxTokens: 1024,
    })
    if err != nil {
    	panic(err)
    }

    fmt.Printf("%+v\n", message.Content)
    ```
  </Accordion>

  <Accordion title="Prompt sistem">
    ```go
    message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    	Model:     anthropic.ModelClaudeOpus4_8,
    	MaxTokens: 1024,
    	System: []anthropic.TextBlockParam{
    		{Text: "Be very serious at all times."},
    	},
    	Messages: messages,
    })
    if err != nil {
    	panic(err)
    }
    fmt.Printf("%+v\n", message.Content)
    ```
  </Accordion>

  <Accordion title="Streaming">
    ```go
    content := "What is a quaternion?"

    stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
    	Model:     anthropic.ModelClaudeOpus4_8,
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
  </Accordion>

  <Accordion title="Pemanggilan alat">
    ```go
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
    		Model:     anthropic.ModelClaudeOpus4_8,
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
    ```
  </Accordion>
</AccordionGroup>

## Field permintaan

Pustaka anthropic menggunakan semantik [`omitzero`](https://tip.golang.org/doc/go1.24#encodingjsonpkgencodingjson) dari rilis `encoding/json` Go 1.24+ untuk field permintaan.

Field primitif yang wajib (`int64`, `string`, dll.) memiliki tag `` `json:"...,required"` ``. Field ini selalu diserialisasi, bahkan nilai nolnya.

Tipe primitif opsional dibungkus dalam `param.Opt[T]`. Field ini dapat diatur dengan konstruktor yang disediakan, `anthropic.String(string)`, `anthropic.Int(int64)`, dll.

Setiap `param.Opt[T]`, map, slice, struct, atau enum string menggunakan tag `` `json:"...,omitzero"` ``. Nilai nolnya dianggap dihilangkan.

Fungsi `param.IsOmitted(any)` dapat mengonfirmasi keberadaan field `omitzero` apa pun.

```go
p := anthropic.ExampleParams{
	ID:   "id_xxx",                // required property
	Name: anthropic.String("..."), // optional property

	Point: anthropic.Point{
		X: 0,                // required field will serialize as 0
		Y: anthropic.Int(1), // optional field will serialize as 1
		// ... field yang tidak wajib dan dihilangkan tidak akan diserialisasi
	},

	Origin: anthropic.Origin{}, // the zero value of [Origin] is considered omitted
}
```

Untuk mengirim `null` alih-alih `param.Opt[T]`, gunakan `param.Null[T]()`. Untuk mengirim `null` alih-alih struct `T`, gunakan `param.NullStruct[T]()`.

```go
p.Name = param.Null[string]()       // 'null' instead of string
p.Point = param.NullStruct[Point]() // 'null' instead of struct

param.IsNull(p.Name)  // true
param.IsNull(p.Point) // true
```

Struct permintaan berisi metode `.SetExtraFields(map[string]any)` yang dapat mengirim field yang tidak sesuai dalam body permintaan. Field tambahan akan menimpa field struct apa pun dengan key yang cocok.

<Warning>
  Untuk alasan keamanan, hanya gunakan `SetExtraFields` dengan data tepercaya.
</Warning>

Untuk mengirim nilai kustom alih-alih struct, gunakan fungsi generik `param.Override` (misalnya, `param.Override[anthropic.FooParams](12)`).

```go
// Dalam kasus di mana API menentukan tipe tertentu,
// tetapi Anda ingin mengirim sesuatu yang lain, gunakan [SetExtraFields]:
p.SetExtraFields(map[string]any{
	"x": 0.01, // send "x" as a float instead of int
})

// Kirim angka alih-alih objek
custom := param.Override[anthropic.FooParams](12)
```

### Union permintaan

Union direpresentasikan sebagai struct dengan field yang diawali dengan "Of" untuk setiap variannya, hanya satu field yang boleh bernilai non-zero. Field non-zero tersebut yang akan diserialisasi.

Subproperti dari union dapat diakses melalui metode pada struct union. Metode ini mengembalikan pointer yang dapat diubah ke data yang mendasarinya, jika ada.

```go
// Hanya satu field yang boleh bernilai non-zero, gunakan param.IsOmitted() untuk memeriksa apakah field telah diatur
type AnimalUnionParam struct {
	OfCat *Cat `json:",omitzero,inline"`
	OfDog *Dog `json:",omitzero,inline"`
}

animal := AnimalUnionParam{
	OfCat: &Cat{
		Name: "Whiskers",
		Owner: PersonParam{
			Address: AddressParam{Street: "3333 Coyote Hill Rd", ZipCode: 0},
		},
	},
}

// Memodifikasi sebuah field
if address := animal.GetOwner().GetAddress(); address != nil {
	address.ZipCode = 94304
}
```

### Deserialisasi params

<Note>
  `param.SetJSON` memerlukan SDK v1.20.0 atau yang lebih baru.
</Note>

Tipe param (tipe yang diakhiri dengan `Param`, seperti `MessageNewParams` atau `ToolUnionParam`) dirancang hanya untuk permintaan keluar. Tipe ini melakukan marshal ke JSON dengan benar tetapi tidak sepenuhnya mendukung deserialisasi bolak-balik (round-trip). Jika Anda melakukan unmarshal JSON mentah ke dalam struct param, field union bertipe seperti `OfBashTool20250124` akan bernilai nil meskipun JSON yang mendasarinya valid.

Jika Anda perlu merekonstruksi params dari JSON mentah (misalnya, dari database, middleware, atau permintaan sebelumnya), panggil `UnmarshalJSON` untuk mengisi field non-union, lalu gunakan `param.SetJSON` untuk melampirkan byte mentah agar serialisasi ulang dilakukan dengan benar:

```go
// Serialisasi params (misalnya, untuk penyimpanan atau penerusan)
b, err := json.Marshal(original)
if err != nil {
	panic(err)
}

// Kemudian, rekonstruksi params dari JSON yang tersimpan
var params anthropic.MessageNewParams
if err := params.UnmarshalJSON(b); err != nil {
	panic(err)
}
param.SetJSON(b, &params)

// params.Model dan field skalar lainnya diisi oleh UnmarshalJSON.
// params.Tools[0].OfBashTool20250124 bernilai nil (keterbatasan union),
// tetapi JSON mentahnya tetap dipertahankan. Ketika params di-marshal lagi
// untuk panggilan API, tools akan diserialisasi dengan benar.
b2, _ := json.Marshal(params)
fmt.Println(string(b) == string(b2)) // true
```

Untuk kasus penggunaan ini, `param.SetJSON` (tersedia sejak v1.20.0) lebih disarankan daripada `param.Override[T](any)` yang lebih umum karena tidak memerlukan penulisan parameter tipe secara eksplisit dan membuat maksud round-trip menjadi jelas.

## Objek respons

Semua field dalam struct respons adalah tipe nilai biasa (bukan pointer atau wrapper). Struct respons juga menyertakan field `JSON` khusus yang berisi metadata tentang setiap properti.

```go
type Animal struct {
	Name   string `json:"name,nullable"`
	Owners int    `json:"owners"`
	Age    int    `json:"age"`
	JSON   struct {
		Name        respjson.Field
		Owners      respjson.Field
		Age         respjson.Field
		ExtraFields map[string]respjson.Field
	} `json:"-"`
}
```

Untuk menangani data opsional, gunakan metode `.Valid()` pada field JSON. `.Valid()` mengembalikan true ketika field tersebut ada, bukan `null`, dan berhasil di-unmarshal.

Jika `.Valid()` bernilai false, field yang bersangkutan akan bernilai nol.

```go
raw := `{"owners": 1, "name": null}`

var res Animal
json.Unmarshal([]byte(raw), &res)

// Mengakses field biasa

res.Owners // 1
res.Name   // ""
res.Age    // 0

// Pemeriksaan field opsional

res.JSON.Owners.Valid() // true
res.JSON.Name.Valid()   // false
res.JSON.Age.Valid()    // false

// Nilai JSON mentah

res.JSON.Owners.Raw()                  // "1"
res.JSON.Name.Raw() == "null"          // true
res.JSON.Name.Raw() == respjson.Null   // true
res.JSON.Age.Raw() == ""               // true
res.JSON.Age.Raw() == respjson.Omitted // true
```

Struct `.JSON` ini juga menyertakan map `ExtraFields` yang berisi properti apa pun dalam respons json yang tidak ditentukan dalam struct. Ini dapat berguna untuk fitur API yang belum tersedia di SDK.

```go
body := res.JSON.ExtraFields["my_unexpected_field"].Raw()
```

### Union respons

Dalam respons, union direpresentasikan oleh struct yang diratakan (flattened) yang berisi semua field yang mungkin dari setiap varian objek. Untuk mengonversinya ke varian, gunakan metode `.AsFooVariant()` atau metode `.AsAny()` jika tersedia.

Jika union nilai respons berisi nilai primitif, field primitif akan berada di samping properti lainnya tetapi diawali dengan `Of` dan memiliki tag `json:"...,inline"`.

```go
type AnimalUnion struct {
	// Dari varian [Dog], [Cat]
	Owner Person `json:"owner"`
	// Dari varian [Dog]
	DogBreed string `json:"dog_breed"`
	// Dari varian [Cat]
	CatBreed string `json:"cat_breed"`
	// ...

	JSON struct {
		Owner respjson.Field
		// ...
	} `json:"-"`
}

// Jika varian animal
if animal.Owner.Address.ZipCode == "" {
	panic("missing zip code")
}

// Switch berdasarkan varian
switch variant := animal.AsAny().(type) {
case Dog:
case Cat:
default:
	panic("unexpected type")
}
```

## Penanganan error

Ketika API mengembalikan kode status non-sukses, SDK mengembalikan error dengan tipe `*anthropic.Error`. Ini berisi nilai `StatusCode`, `*http.Request`, dan `*http.Response` dari permintaan, serta JSON dari body error (seperti objek respons lainnya di SDK). Error ini juga menyertakan `RequestID` dari header respons, yang berguna untuk pemecahan masalah dengan dukungan Anthropic.

Untuk menangani error, gunakan pola `errors.As`:

```go
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
	Model: anthropic.ModelClaudeOpus4_8,
})
if err != nil {
	var apierr *anthropic.Error
	if errors.As(err, &apierr) {
		println("Request ID:", apierr.RequestID)
		println(string(apierr.DumpRequest(true)))  // Prints the serialized HTTP request
		println(string(apierr.DumpResponse(true))) // Prints the serialized HTTP response
	}
	panic(err.Error()) // POST "/v1/messages": 400 Bad Request (Request-ID: req_xxx) { ... }
}
```

Ketika error lain terjadi, error tersebut dikembalikan tanpa dibungkus; misalnya, jika transport HTTP gagal, Anda mungkin menerima `*url.Error` yang membungkus `*net.OpError`.

## Percobaan ulang

Error tertentu akan secara otomatis dicoba ulang 2 kali secara default, dengan exponential backoff singkat. SDK secara default mencoba ulang semua error koneksi, 408 Request Timeout, 409 Conflict, 429 Rate Limit, dan error Internal >=500.

Anda dapat menggunakan opsi `WithMaxRetries` untuk mengonfigurasi atau menonaktifkan ini:

```go
// Konfigurasikan default untuk semua permintaan:
client := anthropic.NewClient(
	option.WithMaxRetries(0), // default is 2
)

// Ganti per permintaan:
// ...
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
			Model: anthropic.ModelClaudeOpus4_8,
		},
		option.WithMaxRetries(5),
	)
```

## Timeout

Permintaan Messages non-streaming mengalami timeout setelah 10 menit secara default; permintaan lain tidak memiliki timeout default. Gunakan context untuk mengonfigurasi timeout untuk siklus hidup permintaan.

Perhatikan bahwa jika permintaan [dicoba ulang](#retries), timeout context tidak dimulai dari awal. Untuk mengatur timeout per percobaan ulang, gunakan `option.WithRequestTimeout()`.

```go
// Ini mengatur timeout untuk permintaan, termasuk semua percobaan ulang.
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
defer cancel()
// ...
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
			Model: anthropic.ModelClaudeOpus4_8,
		},
		// Ini mengatur timeout per percobaan ulang
		option.WithRequestTimeout(20*time.Second),
	)
```

## Permintaan panjang

<Warning>
  Pertimbangkan untuk menggunakan Messages API streaming untuk permintaan yang berjalan lebih lama.
</Warning>

Hindari mengatur nilai `MaxTokens` yang besar tanpa menggunakan streaming karena beberapa jaringan mungkin memutus koneksi idle setelah periode waktu tertentu, yang dapat menyebabkan permintaan gagal atau mengalami [timeout](#timeouts) tanpa menerima respons dari Anthropic.

SDK ini juga akan mengembalikan error jika permintaan non-streaming diperkirakan akan berlangsung lebih dari sekitar 10 menit. Memanggil `.Messages.NewStreaming()` atau [mengatur timeout kustom](#timeouts) akan menonaktifkan error ini.

## Unggahan file

Parameter permintaan yang berkaitan dengan unggahan file dalam permintaan multipart bertipe `io.Reader`. Konten dari `io.Reader` secara default akan dikirim sebagai bagian form multipart dengan nama file "anonymous\_file" dan content-type "application/octet-stream", sehingga pendekatan yang direkomendasikan adalah menentukan content-type kustom dengan helper `anthropic.File(reader io.Reader, filename string, contentType string)`, yang membungkus `io.Reader` apa pun dengan nama file dan content type yang sesuai.

```go
// File dari sistem file
file, err := os.Open("/path/to/file.json")
anthropic.BetaFileUploadParams{
	File: anthropic.File(file, "custom-name.json", "application/json"),
}

// File dari string
anthropic.BetaFileUploadParams{
	File: anthropic.File(strings.NewReader("my file contents"), "custom-name.json", "application/json"),
}
```

Nama file dan content-type juga dapat dikustomisasi dengan mengimplementasikan `Name() string` atau `ContentType() string` pada tipe run-time dari `io.Reader`. Perhatikan bahwa `os.File` mengimplementasikan `Name() string`, sehingga file yang dikembalikan oleh `os.Open` akan dikirim dengan nama file di disk.

## Paginasi

Pustaka ini menyediakan beberapa kemudahan untuk bekerja dengan endpoint daftar yang dipaginasi.

Anda dapat menggunakan metode `.ListAutoPaging()` untuk melakukan iterasi melalui item di semua halaman:

```go
iter := client.Messages.Batches.ListAutoPaging(context.TODO(), anthropic.MessageBatchListParams{
	Limit: anthropic.Int(20),
})
// Secara otomatis mengambil lebih banyak halaman sesuai kebutuhan.
for iter.Next() {
	messageBatch := iter.Current()
	fmt.Printf("%+v\n", messageBatch)
}
if err := iter.Err(); err != nil {
	panic(err.Error())
}
```

Atau Anda dapat menggunakan metode `.List()` sederhana untuk mengambil satu halaman dan menerima objek respons standar dengan metode helper tambahan seperti `.GetNextPage()`:

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

Pustaka ini menggunakan pola opsi fungsional. Fungsi yang didefinisikan dalam package `option` mengembalikan `RequestOption`, yang merupakan closure yang memutasi `RequestConfig`. Opsi ini dapat diberikan ke client atau pada permintaan individual. Misalnya:

```go
client := anthropic.NewClient(
	// Menambahkan header ke setiap permintaan yang dibuat oleh klien
	option.WithHeader("X-Some-Header", "custom_header_info"),
)

client.Messages.New(context.TODO(), // ...,
	// Menimpa header tersebut
	option.WithHeader("X-Some-Header", "some_other_custom_header_info"),
	// Menambahkan field tak terdokumentasi ke body permintaan, menggunakan sintaks sjson
	option.WithJSONSet("some.json.path", map[string]string{"my": "object"}),
)
```

Opsi permintaan `option.WithDebugLog(nil)` mungkin berguna saat melakukan debugging.

Lihat [daftar lengkap opsi permintaan](https://pkg.go.dev/github.com/anthropics/anthropic-sdk-go/option).

## Kustomisasi HTTP client

Untuk middleware permintaan (`option.WithMiddleware`) dan mengganti `http.Client` default (`option.WithHTTPClient`), lihat [middleware SDK](/docs/id/cli-sdks-libraries/middleware).

## Integrasi platform

<Note>
  Untuk panduan penyiapan platform yang terperinci dengan contoh kode, lihat:

  * [Amazon Bedrock](/docs/id/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (legacy)](/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Google Cloud](/docs/id/build-with-claude/claude-on-vertex-ai)
  * [Claude Platform di AWS](/docs/id/build-with-claude/claude-platform-on-aws)
</Note>

Go SDK mendukung platform berikut:

* **Bedrock:** `import "github.com/anthropics/anthropic-sdk-go/bedrock"`. Gunakan `bedrock.NewMantleClient` untuk endpoint Bedrock Messages-API (melakukan streaming melalui SSE), atau `bedrock.WithLoadDefaultConfig(ctx)` / `bedrock.WithConfig(cfg)` (jalur `bedrock-runtime`). Mengimpor package `bedrock` secara global mendaftarkan decoder untuk `application/vnd.amazon.eventstream` dengan lapisan streaming SDK (melalui `init()` package). Ini berlaku baik Anda menggunakan jalur `WithConfig`/`WithLoadDefaultConfig` dari `bedrock-runtime` maupun `NewMantleClient`.
* **Agent Platform:** `import "github.com/anthropics/anthropic-sdk-go/vertex"`. Gunakan `vertex.WithGoogleAuth(ctx, region, projectID)` atau `vertex.WithCredentials(ctx, region, projectID, creds)`.
* **Foundry:** Saat ini tidak didukung di Go SDK. Lihat [Claude di Microsoft Foundry](/docs/id/build-with-claude/claude-in-microsoft-foundry) untuk SDK yang didukung.
* **Claude Platform di AWS:** `import anthropicaws "github.com/anthropics/anthropic-sdk-go/aws"`. Gunakan `anthropicaws.NewClient(ctx, cfg)` dengan nilai `anthropicaws.ClientConfig` untuk membuat client; atur `WorkspaceID` pada config atau variabel lingkungan `ANTHROPIC_AWS_WORKSPACE_ID`. Alias import `anthropicaws` menghindari konflik nama dengan `github.com/aws/aws-sdk-go-v2/aws` ketika keduanya diimpor. Tersedia dalam beta.

Gunakan `bedrock.NewMantleClient` untuk proyek baru; `bedrock.WithLoadDefaultConfig`/`WithConfig` tetap tersedia untuk aplikasi yang sudah ada yang menggunakan API `InvokeModel` Bedrock.

## Penggunaan lanjutan

### Mengakses data respons mentah (misalnya, header respons)

Anda dapat mengakses data respons HTTP mentah dengan menggunakan opsi permintaan `option.WithResponseInto()`. Ini berguna ketika Anda perlu memeriksa header respons, kode status, atau detail lainnya.

```go
// Buat variabel untuk menyimpan respons HTTP
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
		Model: anthropic.ModelClaudeOpus4_8,
	},
	option.WithResponseInto(&response),
)
if err != nil {
	// tangani error
}
fmt.Printf("%+v\n", message)

fmt.Printf("Status Code: %d\n", response.StatusCode)
fmt.Printf("Headers: %+#v\n", response.Header)
```

### Membuat permintaan kustom/tidak terdokumentasi

Pustaka ini diberi tipe untuk akses yang mudah ke API yang terdokumentasi. Jika Anda perlu mengakses endpoint, params, atau properti respons yang tidak terdokumentasi, pustaka ini tetap dapat digunakan.

#### Endpoint tidak terdokumentasi

Untuk membuat permintaan ke endpoint yang tidak terdokumentasi, Anda dapat menggunakan `client.Get`, `client.Post`, dan verb HTTP lainnya. `RequestOptions` pada client, seperti percobaan ulang, akan dihormati saat membuat permintaan ini.

```go
var (
	// params dapat berupa io.Reader, []byte, objek yang dapat diserialisasi encoding/json,
	// atau struct "...Params" yang didefinisikan dalam pustaka ini.
	params map[string]any

	// result dapat berupa []byte, *http.Response, objek yang dapat dideserialisasi encoding/json,
	// atau model yang didefinisikan dalam pustaka ini.
	result *http.Response
)
err := client.Post(context.Background(), "/unspecified", params, &result)
if err != nil {
	// ...
}
```

#### Parameter permintaan tidak terdokumentasi

Untuk membuat permintaan menggunakan parameter yang tidak terdokumentasi, Anda dapat menggunakan metode `option.WithQuerySet()` atau `option.WithJSONSet()`.

```go
params := FooNewParams{
	ID: "id_xxxx",
	Data: FooNewParamsData{
		FirstName: anthropic.String("John"),
	},
}
client.Foo.New(context.Background(), params, option.WithJSONSet("data.last_name", "Doe"))
```

#### Properti respons tidak terdokumentasi

Untuk mengakses properti respons yang tidak terdokumentasi, Anda dapat mengakses JSON mentah dari respons sebagai string dengan `result.JSON.RawJSON()`, atau mendapatkan JSON mentah dari field tertentu pada hasil dengan `result.JSON.Foo.Raw()`.

Field apa pun yang tidak ada pada struct respons akan disimpan dan dapat diakses melalui `result.JSON.ExtraFields`, yang merupakan `map[string]respjson.Field`.

## Semantic versioning

Package ini secara umum mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html), meskipun perubahan tertentu yang tidak kompatibel ke belakang dapat dirilis sebagai versi minor:

1. Perubahan pada internal pustaka yang secara teknis bersifat publik tetapi tidak dimaksudkan atau didokumentasikan untuk penggunaan eksternal.
2. Perubahan yang tidak diperkirakan akan memengaruhi sebagian besar pengguna dalam praktiknya.

Kompatibilitas ke belakang ditangani dengan serius untuk memastikan Anda dapat mengandalkan pengalaman upgrade yang lancar.

Masukan Anda sangat diterima; buka [issue](https://github.com/anthropics/anthropic-sdk-go/issues) dengan pertanyaan, bug, atau saran.

## Sumber daya tambahan

* [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-go)
* [Dokumentasi package Go](https://pkg.go.dev/github.com/anthropics/anthropic-sdk-go)
* [Referensi API](/docs/id/api/overview)
* [Streaming Messages](/docs/id/build-with-claude/streaming)
