---
source: platform
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/go
fetched_at: 2026-08-22T02:26:42.682918Z
sha256: 0d1e0229a194f5601cdc2cd6949989b2ae0cec21d671d544c10c4a21b54d5aee
---

---
title: Go SDK
url: https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/go
description: Instal dan konfigurasikan Anthropic Go SDK dengan pembatalan berbasis context dan functional options
---

Library Anthropic Go menyediakan akses yang mudah ke Claude API dari aplikasi yang ditulis dalam Go.

<Info>
  Untuk dokumentasi fitur API dengan contoh kode, lihat [referensi API](https://platform.claude.com/docs/id/api/overview). Halaman ini membahas fitur dan konfigurasi SDK khusus Go.
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

Library ini memerlukan Go 1.24+.

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
		Model: anthropic.ModelClaudeOpus5,
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

Untuk opsi autentikasi termasuk Workload Identity Federation, lihat [Autentikasi](https://platform.claude.com/docs/id/manage-claude/authentication).

<AccordionGroup>
  <Accordion title="Percakapan">
    ```go
    messages := []anthropic.MessageParam{
    	anthropic.NewUserMessage(anthropic.NewTextBlock("What is my first name?")),
    }

    message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    	Model:     anthropic.ModelClaudeOpus5,
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
    	Model:     anthropic.ModelClaudeOpus5,
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
    	Model:     anthropic.ModelClaudeOpus5,
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
    	Model:     anthropic.ModelClaudeOpus5,
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
    		Model:     anthropic.ModelClaudeOpus5,
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

Library anthropic menggunakan semantik [`omitzero`](https://tip.golang.org/doc/go1.24#encodingjsonpkgencodingjson) dari rilis `encoding/json` Go 1.24+ untuk field permintaan.

Field primitif wajib (seperti `int64` atau `string`) memiliki tag `` `json:"...,required"` ``. Field ini selalu diserialisasi, bahkan nilai nolnya.

Tipe primitif opsional dibungkus dalam `param.Opt[T]`. Field ini dapat diatur dengan konstruktor yang disediakan, seperti `anthropic.String(string)` atau `anthropic.Int(int64)`.

Setiap `param.Opt[T]`, map, slice, struct, atau string enum menggunakan tag `` `json:"...,omitzero"` ``. Nilai nolnya dianggap dihilangkan.

Fungsi `param.IsOmitted(any)` dapat mengonfirmasi keberadaan field `omitzero` apa pun.

```go
p := anthropic.ExampleParams{
	ID:   "id_xxx",                // required property
	Name: anthropic.String("..."), // optional property

	Point: anthropic.Point{
		X: 0,                // required field will serialize as 0
		Y: anthropic.Int(1), // optional field will serialize as 1
		// ... field non-wajib yang dihilangkan tidak akan diserialisasi
	},

	Origin: anthropic.Origin{}, // the zero value of [Origin] is considered omitted
}
```

Untuk mengirim `null` sebagai ganti `param.Opt[T]`, gunakan `param.Null[T]()`. Untuk mengirim `null` sebagai ganti struct `T`, gunakan `param.NullStruct[T]()`.

```go
p.Name = param.Null[string]()       // 'null' instead of string
p.Point = param.NullStruct[Point]() // 'null' instead of struct

param.IsNull(p.Name)  // true
param.IsNull(p.Point) // true
```

Struct permintaan memiliki metode `.SetExtraFields(map[string]any)` yang dapat mengirim field yang tidak sesuai skema dalam body permintaan. Field tambahan menimpa field struct apa pun dengan key yang cocok.

<Warning>
  Demi alasan keamanan, gunakan `SetExtraFields` hanya dengan data tepercaya.
</Warning>

Untuk mengirim nilai kustom sebagai ganti struct, gunakan fungsi generik `param.Override` (misalnya, `param.Override[anthropic.FooParams](12)`).

```go
// Dalam kasus ketika API menentukan tipe tertentu,
// tetapi Anda ingin mengirim sesuatu yang lain, gunakan [SetExtraFields]:
p.SetExtraFields(map[string]any{
	"x": 0.01, // send "x" as a float instead of int
})

// Kirim angka alih-alih objek
custom := param.Override[anthropic.FooParams](12)
```

### Union permintaan

Union direpresentasikan sebagai struct dengan field berawalan "Of" untuk setiap variannya, hanya satu field yang boleh bernilai bukan nol. Field yang bukan nol akan diserialisasi.

Subproperti dari union dapat diakses melalui metode pada struct union. Metode ini mengembalikan pointer yang dapat diubah ke data yang mendasarinya, jika ada.

```go
// Hanya satu field yang boleh bernilai bukan nol, gunakan param.IsOmitted() untuk memeriksa apakah suatu field telah diatur
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

// Mengubah sebuah field
if address := animal.GetOwner().GetAddress(); address != nil {
	address.ZipCode = 94304
}
```

### Deserialisasi param

<Note>
  `param.SetJSON` memerlukan SDK v1.20.0 atau yang lebih baru.
</Note>

Tipe param (tipe yang berakhiran `Param`, seperti `MessageNewParams` atau `ToolUnionParam`) dirancang hanya untuk permintaan keluar. Tipe ini di-marshal dengan benar ke JSON tetapi tidak sepenuhnya mendukung deserialisasi round-trip. Jika Anda meng-unmarshal JSON mentah ke dalam struct param, field union bertipe seperti `OfBashTool20250124` akan bernilai nil meskipun JSON yang mendasarinya valid.

Jika Anda perlu merekonstruksi param dari JSON mentah (misalnya, dari database, middleware, atau permintaan sebelumnya), panggil `UnmarshalJSON` untuk mengisi field non-union, lalu gunakan `param.SetJSON` untuk melampirkan byte mentah agar re-serialisasi berjalan dengan benar:

```go
// Serialisasi params (misalnya, untuk penyimpanan atau penerusan)
b, err := json.Marshal(original)
if err != nil {
	panic(err)
}

// Nanti, rekonstruksi params dari JSON yang tersimpan
var params anthropic.MessageNewParams
if err := params.UnmarshalJSON(b); err != nil {
	panic(err)
}
param.SetJSON(b, &params)

// params.Model dan field skalar lainnya diisi oleh UnmarshalJSON.
// params.Tools[0].OfBashTool20250124 bernilai nil (keterbatasan union),
// tetapi JSON mentah tetap dipertahankan. Saat params di-marshal lagi
// untuk panggilan API, tools diserialisasi dengan benar.
b2, _ := json.Marshal(params)
fmt.Println(string(b) == string(b2)) // true
```

Untuk kasus penggunaan ini, `param.SetJSON` (tersedia sejak v1.20.0) lebih disarankan daripada `param.Override[T](any)` yang lebih umum karena tidak mengharuskan penulisan parameter tipe secara eksplisit dan membuat maksud round-trip menjadi jelas.

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

Dalam respons, union direpresentasikan oleh struct yang diratakan yang berisi semua field yang mungkin dari setiap varian objek. Untuk mengonversinya ke sebuah varian, gunakan metode `.AsFooVariant()` atau metode `.AsAny()` jika tersedia.

Jika union nilai respons berisi nilai primitif, field primitif akan berada berdampingan dengan properti lainnya tetapi berawalan `Of` dan memiliki tag `json:"...,inline"`.

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

Ketika API mengembalikan kode status yang tidak berhasil, SDK mengembalikan error dengan tipe `*anthropic.Error`. Error ini berisi nilai `StatusCode`, `*http.Request`, dan `*http.Response` dari permintaan, beserta JSON dari body error (mirip dengan objek respons lain di SDK). Error ini juga menyertakan `RequestID` dari header respons, yang berguna untuk pemecahan masalah bersama dukungan Anthropic.

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
	Model: anthropic.ModelClaudeOpus5,
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

Error tertentu akan dicoba ulang secara otomatis 2 kali secara default, dengan exponential backoff singkat. Secara default, SDK mencoba ulang semua error koneksi, 408 Request Timeout, 409 Conflict, 429 Rate Limit, dan error Internal >=500.

Anda dapat menggunakan opsi `WithMaxRetries` untuk mengonfigurasi atau menonaktifkan ini:

```go
// Konfigurasikan default untuk semua permintaan:
client := anthropic.NewClient(
	option.WithMaxRetries(0), // default is 2
)

// Timpa per permintaan:
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
			Model: anthropic.ModelClaudeOpus5,
		},
		option.WithMaxRetries(5),
	)
```

## Timeout

Permintaan Messages non-streaming mengalami timeout setelah 10 menit secara default; permintaan lain tidak memiliki timeout default. Gunakan context untuk mengonfigurasi timeout bagi siklus hidup permintaan.

Perhatikan bahwa jika permintaan [dicoba ulang](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/go#retries), timeout context tidak dimulai dari awal. Untuk mengatur timeout per percobaan ulang, gunakan `option.WithRequestTimeout()`.

```go
// Ini menetapkan batas waktu untuk permintaan, termasuk semua percobaan ulang.
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
			Model: anthropic.ModelClaudeOpus5,
		},
		// Ini menetapkan batas waktu per percobaan ulang
		option.WithRequestTimeout(20*time.Second),
	)
```

## Permintaan panjang

<Warning>
  Pertimbangkan untuk menggunakan Messages API streaming untuk permintaan yang berjalan lebih lama.
</Warning>

Hindari mengatur nilai `MaxTokens` yang besar tanpa menggunakan streaming karena beberapa jaringan mungkin memutus koneksi yang menganggur setelah jangka waktu tertentu, yang dapat menyebabkan permintaan gagal atau [timeout](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/go#timeouts) tanpa menerima respons dari Anthropic.

SDK ini juga akan mengembalikan error jika permintaan non-streaming diperkirakan berlangsung lebih dari sekitar 10 menit. Memanggil `.Messages.NewStreaming()` atau [mengatur timeout kustom](https://platform.claude.com/docs/id/cli-sdks-libraries/sdks/go#timeouts) menonaktifkan error ini.

## Unggahan file

Parameter permintaan yang berkaitan dengan unggahan file dalam permintaan multipart bertipe `io.Reader`. Isi dari `io.Reader` secara default akan dikirim sebagai bagian form multipart dengan nama file "anonymous\_file" dan content-type "application/octet-stream", sehingga pendekatan yang disarankan adalah menentukan content-type kustom dengan helper `anthropic.File(reader io.Reader, filename string, contentType string)`, yang membungkus `io.Reader` apa pun dengan nama file dan content type yang sesuai.

```go
// File dari sistem file
file, err := os.Open("/path/to/file.json")
anthropic.FileUploadParams{
	File: anthropic.File(file, "custom-name.json", "application/json"),
}

// File dari string
anthropic.FileUploadParams{
	File: anthropic.File(strings.NewReader("my file contents"), "custom-name.json", "application/json"),
}
```

Nama file dan content-type juga dapat dikustomisasi dengan mengimplementasikan `Name() string` atau `ContentType() string` pada tipe run-time dari `io.Reader`. Perhatikan bahwa `os.File` mengimplementasikan `Name() string`, sehingga file yang dikembalikan oleh `os.Open` akan dikirim dengan nama file di disk.

## Paginasi

Library ini menyediakan beberapa kemudahan untuk bekerja dengan endpoint list yang dipaginasi.

Anda dapat menggunakan metode `.ListAutoPaging()` untuk mengiterasi item di seluruh halaman:

```go
iter := client.Messages.Batches.ListAutoPaging(context.TODO(), anthropic.MessageBatchListParams{
	Limit: anthropic.Int(20),
})
// Secara otomatis mengambil halaman berikutnya sesuai kebutuhan.
for iter.Next() {
	messageBatch := iter.Current()
	fmt.Println(messageBatch.ID)
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
		fmt.Println(batch.ID)
	}
	page, err = page.GetNextPage()
}
if err != nil {
	panic(err.Error())
}
```

## RequestOptions

Library ini menggunakan pola functional options. Fungsi yang didefinisikan dalam package `option` mengembalikan `RequestOption`, yaitu closure yang memutasi `RequestConfig`. Opsi ini dapat diberikan ke client atau pada permintaan individual. Misalnya:

```go
client := anthropic.NewClient(
	// Menambahkan header ke setiap permintaan yang dibuat oleh klien
	option.WithHeader("X-Some-Header", "custom_header_info"),
)

client.Messages.New(context.TODO(), // ...,
	// Menimpa header
	option.WithHeader("X-Some-Header", "some_other_custom_header_info"),
	// Menambahkan field yang tidak terdokumentasi ke body permintaan, menggunakan sintaks sjson
	option.WithJSONSet("some.json.path", map[string]string{"my": "object"}),
)
```

Opsi permintaan `option.WithDebugLog(nil)` mungkin berguna saat debugging.

Lihat [daftar lengkap opsi permintaan](https://pkg.go.dev/github.com/anthropics/anthropic-sdk-go/option).

## Kustomisasi HTTP client

Untuk middleware permintaan (`option.WithMiddleware`) dan mengganti `http.Client` default (`option.WithHTTPClient`), lihat [middleware SDK](https://platform.claude.com/docs/id/cli-sdks-libraries/middleware).

## Integrasi platform

<Note>
  Untuk panduan penyiapan platform yang terperinci dengan contoh kode, lihat:

  * [Amazon Bedrock](https://platform.claude.com/docs/id/build-with-claude/claude-in-amazon-bedrock)
  * [Amazon Bedrock (Opus 4.6 dan sebelumnya)](https://platform.claude.com/docs/id/build-with-claude/claude-on-amazon-bedrock-legacy)
  * [Claude Platform on AWS](https://platform.claude.com/docs/id/build-with-claude/claude-platform-on-aws)
  * [Google Cloud](https://platform.claude.com/docs/id/build-with-claude/claude-on-vertex-ai)
</Note>

Go SDK mendukung platform berikut:

* **Agent Platform:** `import "github.com/anthropics/anthropic-sdk-go/vertex"`. Gunakan `vertex.WithGoogleAuth(ctx, region, projectID)` atau `vertex.WithCredentials(ctx, region, projectID, creds)`.
* **Bedrock:** `import "github.com/anthropics/anthropic-sdk-go/bedrock"`. Gunakan `bedrock.NewMantleClient` untuk endpoint Bedrock Messages-API (streaming melalui SSE), atau `bedrock.WithLoadDefaultConfig(ctx)` / `bedrock.WithConfig(cfg)` (jalur `bedrock-runtime`). Mengimpor package `bedrock` secara global mendaftarkan decoder untuk `application/vnd.amazon.eventstream` pada lapisan streaming SDK (melalui `init()` package). Ini berlaku baik Anda menggunakan jalur `bedrock-runtime` `WithConfig`/`WithLoadDefaultConfig` maupun `NewMantleClient`.
* **Claude Platform on AWS:** `import anthropicaws "github.com/anthropics/anthropic-sdk-go/aws"`. Gunakan `anthropicaws.NewClient(ctx, cfg)` dengan nilai `anthropicaws.ClientConfig` untuk membuat client; atur `WorkspaceID` pada config atau variabel lingkungan `ANTHROPIC_AWS_WORKSPACE_ID`. Alias impor `anthropicaws` menghindari tabrakan nama dengan `github.com/aws/aws-sdk-go-v2/aws` ketika keduanya diimpor. Tersedia dalam beta.
* **Foundry:** Saat ini tidak didukung di Go SDK. Lihat [Claude in Microsoft Foundry](https://platform.claude.com/docs/id/build-with-claude/claude-in-microsoft-foundry) untuk SDK yang didukung.

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
		Model: anthropic.ModelClaudeOpus5,
	},
	option.WithResponseInto(&response),
)
if err != nil {
	// tangani error
}
fmt.Printf("%+v\n", message.Content)

fmt.Printf("Status Code: %d\n", response.StatusCode)
fmt.Printf("Headers: %+#v\n", response.Header)
```

### Membuat permintaan kustom/tidak terdokumentasi

Library ini bertipe untuk akses yang mudah ke API yang terdokumentasi. Jika Anda perlu mengakses endpoint, param, atau properti respons yang tidak terdokumentasi, library ini tetap dapat digunakan.

#### Endpoint tidak terdokumentasi

Untuk membuat permintaan ke endpoint yang tidak terdokumentasi, Anda dapat menggunakan `client.Get`, `client.Post`, dan verb HTTP lainnya. `RequestOptions` pada client, seperti percobaan ulang, akan dipatuhi saat membuat permintaan ini.

```go
var (
	// params dapat berupa io.Reader, []byte, objek yang dapat diserialisasi dengan encoding/json,
	// atau struct "...Params" yang didefinisikan dalam library ini.
	params map[string]any

	// result dapat berupa []byte, *http.Response, objek yang dapat dideserialisasi dengan encoding/json,
	// atau model yang didefinisikan dalam library ini.
	result *http.Response
)
err := client.Post(context.Background(), "/unspecified", params, &result)
if err != nil {
	// ...
}
```

#### Param permintaan tidak terdokumentasi

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

Field apa pun yang tidak ada pada struct respons disimpan dan dapat diakses melalui `result.JSON.ExtraFields`, yang merupakan `map[string]respjson.Field`.

## Semantic versioning

Package ini secara umum mengikuti konvensi [SemVer](https://semver.org/spec/v2.0.0.html), meskipun perubahan tertentu yang tidak kompatibel ke belakang mungkin dirilis sebagai versi minor:

1. Perubahan pada internal library yang secara teknis publik tetapi tidak dimaksudkan atau didokumentasikan untuk penggunaan eksternal.
2. Perubahan yang diperkirakan tidak berdampak pada sebagian besar pengguna dalam praktiknya.

Kompatibilitas ke belakang ditangani dengan serius untuk memastikan Anda dapat mengandalkan pengalaman upgrade yang lancar.

Masukan Anda sangat kami harapkan; buka [issue](https://github.com/anthropics/anthropic-sdk-go/issues) untuk pertanyaan, bug, atau saran.

## Sumber daya tambahan

* [Repositori GitHub](https://github.com/anthropics/anthropic-sdk-go)
* [Dokumentasi package Go](https://pkg.go.dev/github.com/anthropics/anthropic-sdk-go)
* [Referensi API](https://platform.claude.com/docs/id/api/overview)
* [Streaming Messages](https://platform.claude.com/docs/id/build-with-claude/streaming)
