---
source: platform
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk
fetched_at: 2026-10-16T02:19:48.985501Z
sha256: 4110c7a3d25c8dbf52713da7597f0d90a28b6ee4ee9f3526fa963ad3e5265408
---

---
title: Penggunaan browser dan komputer dengan toolset SDK
url: https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk
description: Jalankan alat penggunaan browser atau alat penggunaan komputer dari SDK Python atau TypeScript. SDK menjalankan loop dan pemeriksaan yang Anda konfigurasikan, dan Anda menyediakan browser atau desktopnya.
---

SDK Python dan TypeScript menyertakan sebuah kelas untuk [alat penggunaan browser](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool) dan sebuah kelas untuk [alat penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool). Anda membuat subclass dari salah satunya dan menulis satu metode per alat anggota, seperti `navigate` atau `left_click`, terhadap otomatisasi browser atau desktop Anda sendiri. SDK merutekan setiap panggilan, menjalankan kebijakan yang Anda berikan, meminta callback persetujuan Anda, dan membangun setiap `tool_result`.

Sebagian besar halaman ini menggunakan kelas browser. [Computer toolset](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#computer-toolset) membahas kelas komputer dan apa yang berbeda untuknya.

SDK tidak menyertakan browser, desktop, driver siap pakai, atau kebijakan URL. [Contoh CDP minimal](https://github.com/anthropics/claude-quickstarts/tree/main/browser-toolset) ada di repositori claude-quickstarts, dalam Python dan TypeScript. Contoh ini mengendalikan Chromium melalui Chrome DevTools Protocol (CDP), dan bukan kode produksi.

<Note>
  Kelas browser toolset berstatus beta dan tersedia di [SDK Python](https://github.com/anthropics/anthropic-sdk-python/blob/main/browser-toolset.md) dan [SDK TypeScript](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/browser-toolset.md). Kelas computer toolset berstatus beta di SDK yang sama, yang memiliki [panduan computer toolset Python](https://github.com/anthropics/anthropic-sdk-python/blob/main/computer-toolset.md) dan [panduan computer toolset TypeScript](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/computer-toolset.md). Setiap kelas berjalan dengan [tool runner](https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-runner) atau dalam loop yang Anda tulis sendiri.
</Note>

## Integrasi mitra

Browser Use, Browserbase, Daytona, dan E2B menerbitkan integrasi mereka sendiri dengan toolset SDK.

### Browser Use

* [Dokumentasi Browser Use](https://docs.browser-use.com/open-source/customize/integrations/toolsets-for-claude)
* [Quickstart Browser Use](https://github.com/browser-use/browser-use/tree/main/examples/integrations/toolsets-for-claude)

### Browserbase

* [Dokumentasi Browserbase Stagehand](https://docs.stagehand.dev/v4/integrations/agent-frameworks/claude-cua-toolset-quickstart)
* [Toolset Browserbase](https://github.com/browserbase/claude-cua-toolset)

### Daytona

* [Panduan Daytona](https://www.daytona.io/docs/en/guides/claude/claude-draws-daytona-sandbox/)

### E2B

* [Dokumentasi E2B](https://docs.e2b.dev/agents/claude-toolsets)
* [Contoh E2B](https://github.com/e2b-dev/e2b-cookbook/tree/main/examples/anthropic-computer-use-orangehrm-js)

## Mulai cepat

Driver adalah subclass Anda dari `BetaAbstractBrowserToolset20260801`. Driver ini mengimplementasikan `navigate`, `screenshot`, dan `left_click`, ditambah `_browser_state` (typescript: `browserState`), laporan status yang dibutuhkan setiap driver. Dalam contoh, `backend` mewakili wrapper Anda sendiri di sekitar pustaka otomatisasi browser, seperti Playwright. Kebijakan URL-nya adalah contoh. [Menulis kebijakan URL](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#write-a-url-policy) menjelaskannya.

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  import re
  from urllib.parse import urlsplit

  from anthropic import Anthropic
  from anthropic.tools import ToolError
  from anthropic.tools.browser import (
      BetaAbstractBrowserToolset20260801,
      BetaBrowserNavigateResult,
      BetaBrowserState,
      BetaScreenshotResult,
      BetaToolsetCallContext,
      BetaURLContext,
  )
  from anthropic.types.beta import (
      BetaBrowserLeftClickInput,
      BetaBrowserNavigateInput,
      BetaBrowserScreenshotInput,
      BetaBrowserStateTabEntryParam,
  )


  class MyBrowser(BetaAbstractBrowserToolset20260801):
      def __init__(self, backend, **options):
          super().__init__(**options)
          self.backend = backend

      def _browser_state(self, context: BetaToolsetCallContext) -> BetaBrowserState:
          return BetaBrowserState(
              tabs=[
                  BetaBrowserStateTabEntryParam(
                      tab_id=tab.id,
                      title=tab.title,
                      url=tab.url,
                      active=tab.id == self.backend.active,
                  )
                  for tab in self.backend.tabs()
              ],
              state_changes=self.backend.drain_changes(),
          )

      def navigate(
          self, context: BetaToolsetCallContext, input: BetaBrowserNavigateInput
      ) -> BetaBrowserNavigateResult:
          # input.url berisi "back", "forward", "reload", atau URL yang diizinkan oleh kebijakan URL
          # Anda, persis seperti yang ditulis Claude. Seperti is_allowed, backend.goto menambahkan https://
          # ke URL yang tidak diawali dengan skema.
          page = self.backend.goto(input.url, input.tab_id)
          return BetaBrowserNavigateResult(
              url=page.url, status=page.status, title=page.title
          )

      def screenshot(
          self, context: BetaToolsetCallContext, input: BetaBrowserScreenshotInput
      ) -> BetaScreenshotResult:
          data = self.backend.png_base64(input.tab_id)
          return BetaScreenshotResult(data=data, media_type="image/png")

      def left_click(
          self, context: BetaToolsetCallContext, input: BetaBrowserLeftClickInput
      ) -> None:
          # Tidak ada yang dikembalikan: Claude membaca "Clicked."
          self.backend.click(input.target, input.tab_id)

      def close(self) -> None:
          super().close()  # first, so no call is still using the browser when it closes
          if not self.backend.closed:
              self.backend.close()


  ALLOWED_HOSTS = ("example.com", "iana.org")
  SCHEME_PREFIX = re.compile(r"[a-z][a-z0-9+.-]*:", re.IGNORECASE)


  def is_allowed(url: str) -> bool:
      # Sekadar contoh, bukan kebijakan untuk produksi. Lihat "Write a URL policy".
      if url.lower() == "about:blank":
          return True
      with_scheme = url if SCHEME_PREFIX.match(url) else f"https://{url}"
      # Browser membaca "\" sebagai "/" dalam URL web.
      try:
          parts = urlsplit(with_scheme.replace("\\", "/"))
      except ValueError:
          return False
      host = parts.hostname or ""
      listed = any(host == name or host.endswith(f".{name}") for name in ALLOWED_HOSTS)
      return parts.scheme in ("http", "https") and listed


  def url_policy(context: BetaURLContext, url: str) -> None:
      if not is_allowed(url):
          raise ToolError(f"blocked: {url} is not on an allowed host")


  client = Anthropic()
  with MyBrowser(backend, url_policy=url_policy) as browser:
      runner = client.beta.messages.tool_runner(
          model="claude-opus-5-5",
          max_tokens=1024,
          tools=[browser],
          messages=[
              {
                  "role": "user",
                  "content": "Open example.com and tell me the page heading.",
              }
          ],
          stream=True,
          run_tools_eagerly=True,  # so a call can start before the response ends
      )
      for stream in runner:
          print(stream.get_final_message())
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import {
    BetaAbstractBrowserToolset20260801,
    type BetaBrowserNavigateResult,
    type BetaBrowserToolsetOptions,
    type BetaScreenshotResult,
    type BetaToolsetCallContext,
    type BetaURLContext,
    ToolError
  } from "@anthropic-ai/sdk/helpers/beta/toolsets";
  import type {
    BetaBrowserLeftClickInput,
    BetaBrowserNavigateInput,
    BetaBrowserScreenshotInput
  } from "@anthropic-ai/sdk/resources/beta";

  class MyBrowser extends BetaAbstractBrowserToolset20260801 {
    constructor(
      private backend: Backend,
      options: Omit<BetaBrowserToolsetOptions, "browserState"> = {}
    ) {
      super({
        ...options,
        // Wajib: setiap tab yang terbuka, dan apa yang berubah sejak laporan terakhir.
        browserState: () => ({
          tabs: backend.tabs().map((tab) => ({
            tab_id: tab.id,
            title: tab.title,
            url: tab.url,
            active: tab.id === backend.active
          })),
          state_changes: backend.drainChanges()
        })
      });
    }

    protected override async navigate(
      ctx: BetaToolsetCallContext,
      input: BetaBrowserNavigateInput
    ): Promise<BetaBrowserNavigateResult> {
      // input.url berisi "back", "forward", "reload", atau URL yang diizinkan oleh kebijakan URL
      // Anda, sebagaimana ditulis Claude. Seperti isAllowed, backend.goto menambahkan https:// ke
      // URL yang tidak diawali dengan skema.
      const page = await this.backend.goto(input.url, input.tab_id);
      return { url: page.url, status: page.status, title: page.title };
    }

    protected override async screenshot(
      ctx: BetaToolsetCallContext,
      input: BetaBrowserScreenshotInput
    ): Promise<BetaScreenshotResult> {
      return { data: await this.backend.pngBase64(input.tab_id), mediaType: "image/png" };
    }

    protected override async left_click(
      ctx: BetaToolsetCallContext,
      input: BetaBrowserLeftClickInput
    ): Promise<void> {
      // Tidak ada yang dikembalikan: Claude membaca "Clicked."
      await this.backend.click(input.target, input.tab_id);
    }

    override async close(): Promise<void> {
      await super.close(); // first, so no call is still using the browser when it closes
      if (!this.backend.closed) await this.backend.close();
    }
  }

  const ALLOWED_HOSTS = ["example.com", "iana.org"];
  const SCHEME_PREFIX = /^[a-z][a-z0-9+.-]*:/i;

  // Sebuah contoh, bukan kebijakan produksi. Lihat "Write a URL policy".
  function isAllowed(url: string): boolean {
    if (url.toLowerCase() === "about:blank") return true;
    const withScheme = SCHEME_PREFIX.test(url) ? url : `https://${url}`;
    // Browser membaca "\" sebagai "/" dalam URL web.
    const parsed = URL.parse(withScheme.replaceAll("\\", "/"));
    const host = parsed?.hostname ?? "";
    const listed = ALLOWED_HOSTS.some((name) => host === name || host.endsWith(`.${name}`));
    return (parsed?.protocol === "http:" || parsed?.protocol === "https:") && listed;
  }

  function urlPolicy(ctx: BetaURLContext, url: string): void {
    if (!isAllowed(url)) throw new ToolError(`blocked: ${url} is not on an allowed host`);
  }

  const client = new Anthropic();
  const browser = new MyBrowser(backend, { urlPolicy });
  try {
    const runner = client.beta.messages.toolRunner({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      tools: [browser],
      messages: [{ role: "user", content: "Open example.com and tell me the page heading." }],
      stream: true,
      runToolsEagerly: true // so a call can start before the response ends
    });
    for await (const stream of runner) console.log(await stream.finalMessage());
  } finally {
    await browser.close();
  }
  ```
</CodeGroup>

Teruskan instance driver itu sendiri sebagai entri `tools`. Anggota yang tidak Anda implementasikan dikirim ke API dalam keadaan dinonaktifkan. Jika Claude tetap memanggilnya, SDK mengembalikan error, dan run tetap berlanjut. Meng-override `execute` mengubah anggota mana yang dikirim dalam keadaan dinonaktifkan ([Menambahkan hook sebelum dan sesudah](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#add-before-and-after-hooks)). Runner tidak pernah menutup toolset, sehingga satu instance dapat melayani beberapa run. Tutup toolset setelah Anda selesai.

Contoh ini mengaktifkan early start (mulai lebih awal). Lihat [Memulai panggilan saat respons sedang di-streaming](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#start-calls-while-the-response-streams).

<Warning>
  Lakukan dua hal ini sebelum Anda menjalankan driver terhadap apa pun selain browser sekali pakai:

  * [Tulis kebijakan URL](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#write-a-url-policy), dan blokir rentang jaringan privat serta alamat metadata cloud `169.254.169.254` dengan [aturan egress pada container](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#put-egress-policy-on-the-container). Tanpa kebijakan URL, SDK tidak memeriksa URL apa pun. Aturan egress di luar container tidak melihat loopback, sehingga sebuah halaman masih dapat menjangkau apa pun yang mendengarkan di container browser.
  * Gunakan profil browser yang tidak masuk (signed in) ke akun mana pun yang data atau tindakannya tidak akan Anda serahkan kepada Claude. Lihat [Mengisolasi host browser](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#isolate-the-browser-host).
</Warning>

## Menyesuaikan driver

### Mengaktifkan atau menonaktifkan anggota

`configs` menerima pengaturan per anggota yang dijelaskan di [Mengonfigurasi toolset](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#configure-the-toolset). Cantumkan hanya anggota yang Anda ubah:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  # MyBrowser yang juga mengimplementasikan read_console
  browser = MyBrowser(
      backend, configs={"read_console": {"enabled": True}, "navigate": {"enabled": False}}
  )
  ```

  ```typescript TypeScript
  // MyBrowser yang juga mengimplementasikan read_console
  const browser = new MyBrowser(backend, {
    configs: { read_console: { enabled: true }, navigate: { enabled: false } }
  });
  ```
</CodeGroup>

SDK menolak panggilan ke anggota yang dinonaktifkan sebelum kode Anda berjalan. Mengaktifkan anggota yang tidak diimplementasikan oleh kelas Anda merupakan error konfigurasi, kecuali kelas tersebut meng-override `execute`.

### Menambahkan hook sebelum dan sesudah

Override `execute` dan panggil `execute` milik parent. Kode sebelum panggilan itu berjalan setelah [kebijakan URL](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#write-a-url-policy), [kebijakan file](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#confine-uploads-and-downloads), dan [`confirm`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#gate-consequential-members), dan kode tersebut dapat mengubah input. SDK tidak memeriksa input yang diubah lagi. Kode setelah panggilan menerima hasilnya, dan dapat mengubah hasil tersebut. Raise `ToolError` (throw di TypeScript) untuk menolak panggilan.

Meng-override `execute` mengubah anggota mana yang ditawarkan kepada Claude. SDK menganggap setiap anggota sudah diimplementasikan, sehingga Claude ditawari setiap anggota yang aktif secara default. `MyBrowser` dari mulai cepat melayani tiga anggota, sehingga `TracedBrowser` berikut menawarkan kepada Claude anggota-anggota yang tidak dapat dilayaninya. Nonaktifkan anggota tersebut dengan `configs` sebelum Anda menggunakannya.

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  import time


  class TracedBrowser(MyBrowser):
      def execute(self, context, name, input):
          started = time.monotonic()
          result = super().execute(context, name, input)
          elapsed_ms = (time.monotonic() - started) * 1000
          call_id = context.tool_use.id if context.tool_use else "-"
          log.info("%s %s %.0fms", call_id, name, elapsed_ms)
          return redact(result) if name == "get_page_text" else result
  ```

  ```typescript TypeScript
  import type { BetaToolsetCallContext } from "@anthropic-ai/sdk/helpers/beta/toolsets";
  import type {
    BetaBrowserMemberInput,
    BetaBrowserMemberName
  } from "@anthropic-ai/sdk/resources/beta";

  class TracedBrowser extends MyBrowser {
    protected override async execute(
      ctx: BetaToolsetCallContext,
      name: BetaBrowserMemberName,
      input: BetaBrowserMemberInput
    ) {
      const started = performance.now();
      const result = await super.execute(ctx, name, input);
      log.info(`${ctx.toolUse?.id ?? "-"} ${name} ${Math.round(performance.now() - started)}ms`);
      return name === "get_page_text" ? redact(result as string) : result;
    }
  }
  ```
</CodeGroup>

## Mengimplementasikan driver

Override anggota yang didukung browser Anda. Setiap anggota menerima konteks panggilan dan input anggota sebagai objek bertipe, seperti `BetaBrowserNavigateInput`. Tipe input berasal dari `anthropic.types.beta` (typescript: `@anthropic-ai/sdk/resources/beta`). [Alat anggota](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#member-tools) mencantumkan field setiap input.

Di TypeScript, tulis anggota sebagai metode, bukan field arrow-function, karena SDK menemukannya pada prototype. Tulis anggota `type` sebagai `type_` di TypeScript. Di Python, namanya `type`.

### Mengembalikan hasil

Apa yang dikembalikan anggota menentukan apa yang dibaca Claude. Hasil yang berhasil diakhiri dengan blok `browser_state` yang dibangun dari laporan state Anda. Hasil error tidak membawa blok tersebut.

| Anggota                                                                                 | Mengembalikan                                                                                            | Yang dibaca Claude                                                                              |
| --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `screenshot`, `zoom`                                                                    | `BetaScreenshotResult`                                                                                   | Satu blok gambar                                                                                |
| `navigate`                                                                              | `BetaBrowserNavigateResult`                                                                              | `Navigated to {url} — {title} (HTTP {status})`                                                  |
| `new_tab`, `switch_tab`, `list_tabs`, `close_tab`                                       | Sebuah entri tab (`new_tab`, `switch_tab`), daftar entri tab (`list_tabs`), atau tidak ada (`close_tab`) | Blok `browser_state` saja                                                                       |
| `read_page`, `get_page_text`, `find`, `read_console`, `read_network`, `javascript_exec` | Sebuah string                                                                                            | String tersebut, atau `(empty)` untuk string kosong                                             |
| Setiap anggota lainnya                                                                  | Tidak ada, atau satu baris teks                                                                          | Konfirmasi singkat, seperti `Clicked.`, lalu baris yang dikembalikan dalam blok teks tersendiri |

### Melaporkan state browser

SDK memanggil `_browser_state` (typescript: `browserState`) setelah setiap panggilan yang mengembalikan hasil, termasuk panggilan yang ditolak dan gagal. Kembalikan setiap tab yang terbuka, dan apa yang berubah sejak laporan terakhir:

* Tab yang dibuka dan event unduhan.
* Sebuah `BetaNavigationRefused` untuk setiap navigasi yang diblokir oleh [request hook](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#intercept-requests-in-the-driver) Anda.
* Sebuah `BetaDialogDismissed` untuk setiap dialog native yang ditutup oleh driver Anda.

Masukkan semua ini ke dalam `state_changes`. Di Python, `BetaNavigationRefused()` dan `BetaDialogDismissed(kind=..., message=...)` berasal dari `anthropic.tools.browser`. Di TypeScript, keduanya adalah `{ type: "navigation_refused" }` dan `{ type: "dialog_dismissed", kind, message }`.

Dua yang terakhir bukan perubahan state API. SDK melaporkannya kepada Claude sebagai teks di luar blok `browser_state`: satu baris untuk semua navigasi yang ditolak, yang tidak menyebutkan URL, dan satu baris untuk masing-masing dari tiga dialog pertama yang ditutup, lalu jumlah dialog lainnya.

Ketika ada tab yang terbuka, tepat satu tab harus aktif. Setiap anggota yang menerima `tab_id` harus bertindak pada tab yang disebutkannya. Batasan API pada laporan tercantum di [Melacak tab dengan `browser_state`](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#track-tabs-and-page-state).

Claude membaca URL setiap tab, URL setiap unduhan, dan URL yang dikembalikan `navigate` Anda, sebagaimana ditulis oleh driver Anda. SDK tidak mem-parse URL ini. SDK mengubah jeda baris dan karakter kontrol lainnya menjadi spasi, memangkas ujung-ujungnya, dan memotong setiap URL pada 4.096 karakter. Jadi isi URL `data:`, path URL `file:`, serta nama pengguna atau kata sandi dalam URL semuanya sampai ke Claude.

### Menangani error

| Di-raise oleh anggota atau SDK | Yang dibaca Claude                                                                      | Run       |
| ------------------------------ | --------------------------------------------------------------------------------------- | --------- |
| `ToolError`                    | Pesannya, sebagai hasil error                                                           | Berlanjut |
| `ToolsetUsageError`            | Tidak ada                                                                               | Berhenti  |
| Exception lainnya              | `ClassName: message` di Python atau `Error: message` di TypeScript, sebagai hasil error | Berlanjut |

SDK me-raise `ToolsetUsageError` untuk error konfigurasi, penyalahgunaan SDK selama panggilan, atau panggilan setelah `close`. SDK juga me-raise-nya ketika `_browser_state` (typescript: `browserState`) me-raise exception apa pun, bahkan `ToolError`. Tool runner dan `tool_result` (typescript: `toolResult`) tidak menangkapnya, sehingga exception tersebut sampai ke pemanggilnya.

SDK tidak menyembunyikan path lokal dalam teks error anggota, dalam baris yang dikembalikan oleh aksi seperti `left_click`, dalam error unduhan yang gagal, atau dalam pesan dialog yang ditutup.

`ToolError` dari kebijakan URL, kebijakan file, atau callable `confirm` Anda sampai ke Claude sebagaimana ditulis, jadi jangan sertakan path lokal dalam teksnya. Tangkap exception di anggota Anda, dan raise `ToolError` (throw di TypeScript) dengan teks Anda sendiri.

### Memulai panggilan saat respons sedang di-streaming

Secara default, tool runner menjalankan panggilan dalam satu giliran setelah respons Claude berakhir. Dengan early start, tool runner dapat memulai panggilan browser atau komputer saat respons masih di-streaming.

Untuk mengaktifkannya, berikan `stream=True` (typescript: `stream: true`) dan `run_tools_eagerly=True` (typescript: `runToolsEagerly: true`) ke tool runner, seperti pada contoh mulai cepat. Dengan `stream`, setiap iterasi loop Anda atas runner memberi Anda sebuah stream, bukan pesan.

Early start mengubah kapan panggilan dapat dimulai, bukan cara toolset menjalankannya:

* **Pemeriksaan tetap berjalan lebih dulu:** SDK memanggil kebijakan URL, kebijakan file, dan `confirm` Anda sebelum panggilan berjalan. Dengan early start, SDK dapat memanggil `confirm` saat respons masih di-streaming.
* **Panggilan tetap berjalan satu per satu:** Sebuah toolset menjalankan panggilannya sesuai urutan yang ditulis Claude. Panggilan yang gagal tetap menghentikan panggilan berikutnya dari toolset tersebut dalam giliran itu.
* **Panggilan yang sudah dimulai tidak dapat dibatalkan:** Jika respons kemudian terpotong, misalnya pada `max_tokens`, atau loop Anda berhenti lebih awal, aksi tersebut tetap terjadi, dan Claude tidak pernah membaca hasilnya.

### Menjalankan tanpa tool runner

Berikan instance di `tools` (`browser.toJSON()` di TypeScript), dan jawab setiap panggilan anggota dengan `tool_result` (typescript: `toolResult`). Alat penggunaan browser mengharuskan Anda berhenti pada panggilan gagal pertama ([Tindakan batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#batch-actions)). Setelah panggilan gagal, loop ini menjawab panggilan berikutnya dalam giliran tersebut tanpa menjalankannya:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  from anthropic.types.beta import BetaMessageParam, BetaToolResultBlockParam

  NOT_EXECUTED = "Not executed: an earlier action in this turn failed."
  MAX_TURNS = 10

  with MyBrowser(backend, url_policy=url_policy) as browser:
      messages: list[BetaMessageParam] = [{"role": "user", "content": "Open example.com"}]
      for _ in range(MAX_TURNS):
          response = client.beta.messages.create(
              model="claude-opus-5-5",
              max_tokens=1024,
              tools=[browser],
              messages=messages,
          )
          messages.append({"role": "assistant", "content": response.content})
          calls = [
              block
              for block in response.content
              if block.type == "tool_use" and block.toolset_name == browser.toolset_name
          ]
          if not calls:
              break
          results: list[BetaToolResultBlockParam] = []
          failed = False
          for call in calls:
              if failed:
                  # Setelah panggilan gagal, sisa giliran dijawab, bukan dijalankan.
                  results.append(
                      {
                          "type": "tool_result",
                          "tool_use_id": call.id,
                          "toolset_name": call.toolset_name,
                          "content": NOT_EXECUTED,
                          "is_error": True,
                      }
                  )
                  continue
              result = browser.tool_result(call)
              failed = bool(result.get("is_error"))
              results.append(result)
          messages.append({"role": "user", "content": results})
  ```

  ```typescript TypeScript
  const NOT_EXECUTED = "Not executed: an earlier action in this turn failed.";
  const MAX_TURNS = 10;

  const browser = new MyBrowser(backend, { urlPolicy });
  try {
    const messages: Anthropic.Beta.BetaMessageParam[] = [
      { role: "user", content: "Open example.com" }
    ];
    for (let turn = 0; turn < MAX_TURNS; turn++) {
      const response = await client.beta.messages.create({
        model: "claude-opus-5-5",
        max_tokens: 1024,
        tools: [browser.toJSON()],
        messages
      });
      messages.push({ role: "assistant", content: response.content });
      const calls = response.content.filter(
        (block): block is Anthropic.Beta.BetaToolUseBlock =>
          block.type === "tool_use" && block.toolset_name === browser.toolsetName
      );
      if (calls.length === 0) break;
      const results: Anthropic.Beta.BetaToolResultBlockParam[] = [];
      let failed = false;
      for (const call of calls) {
        if (failed) {
          // Setelah satu panggilan gagal, sisa giliran ini hanya dijawab, tidak dijalankan.
          results.push({
            type: "tool_result",
            tool_use_id: call.id,
            toolset_name: call.toolset_name,
            content: NOT_EXECUTED,
            is_error: true
          });
          continue;
        }
        const result = await browser.toolResult(call);
        failed = result.is_error === true;
        results.push(result);
      }
      messages.push({ role: "user", content: results });
    }
  } finally {
    await browser.close();
  }
  ```
</CodeGroup>

Setiap jawaban untuk panggilan yang dilewati membawa `is_error`, `toolset_name` dari panggilan tersebut, dan teks persis yang diwajibkan oleh [Tindakan batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#batch-actions). Tool runner mengirimkan jawaban yang sama.

## Menjalankan toolset dengan aman

Tindakan Claude berikutnya bergantung pada halaman yang dibacanya. Sebuah halaman, atau teks yang disuntikkan ke dalamnya, dapat mencoba menjangkau layanan internal atau menarik file dari host. Halaman tersebut juga dapat mencoba memicu tindakan dengan efek nyata. Sebelum Anda menjalankan driver terhadap apa pun selain browser sekali pakai, lakukan enam langkah berikut:

1. [Tulis kebijakan URL](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#write-a-url-policy) yang menolak setiap URL `navigate` yang tidak dibutuhkan tugas.
2. [Intersep permintaan di driver](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#intercept-requests-in-the-driver), dan periksa setiap request dengan aturan yang sama.
3. [Terapkan kebijakan egress pada container](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#put-egress-policy-on-the-container), sehingga jaringan memblokir apa yang tidak dapat dilihat driver.
4. [Batasi unggahan dan unduhan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#confine-uploads-and-downloads), atau biarkan unggahan nonaktif.
5. [Batasi anggota yang berdampak](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#gate-consequential-members) dengan `confirm`.
6. [Isolasi host browser](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#isolate-the-browser-host) dalam container atau VM khusus untuk setiap sesi.

SDK menerapkan langkah 1, 4, dan 5 melalui kebijakan dan callable yang Anda berikan. Langkah 2, 3, dan 6 menjadi tanggung jawab driver dan deployment Anda. Tindakan pencegahan di [Pertimbangan keamanan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#security-considerations) juga berlaku.

<Note>
  Classifier "prompt injection" (injeksi prompt) milik Anthropic, yang dijelaskan di [Pertimbangan keamanan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#security-considerations), saat ini tidak berjalan pada permintaan toolset browser yang dikirim melalui Amazon Bedrock.
</Note>

### Menulis kebijakan URL

<Warning>
  Tanpa kebijakan URL, SDK tidak memeriksa URL apa pun, dan API tidak memfilter URL yang dibuka Claude. Bahkan dengan kebijakan, tautan yang diklik Claude atau sebuah redirect dapat membawa browser ke loopback (`localhost`, `127.0.0.1`), ke alamat link-local seperti alamat metadata cloud `169.254.169.254`, dan ke rentang jaringan privat. [Aturan egress pada container](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#put-egress-policy-on-the-container) dapat memblokir alamat link-local dan privat. Aturan yang diterapkan di luar container tidak dapat memblokir loopback.

  SDK tidak memeriksa skema URL, sehingga driver Anda harus menolak setiap skema yang tidak dimaksudkan untuk dibuka, seperti `javascript:`, `view-source:`, `data:`, dan `file:`. Sebagian besar driver hanya membutuhkan `http` dan `https`. Contoh kebijakan di bawah hanya mengizinkan URL `http` dan `https`, ditambah `about:blank`.

  URL `file:` memungkinkan Claude membaca file di host browser. URL `javascript:` menjalankan skrip di halaman saat ini, bahkan ketika `javascript_exec` nonaktif. Aturan egress tidak menghentikan keduanya.
</Warning>

Kebijakan URL adalah fungsi yang Anda berikan sebagai `url_policy` (typescript: `urlPolicy`). Anda yang menulis kebijakan tersebut, dan Anda bertanggung jawab untuk membuatnya siap produksi. Sebelum `navigate` Anda berjalan, SDK memanggil kebijakan dengan konteks panggilan dan URL sebagaimana ditulis Claude.

Jangan kembalikan apa pun untuk mengizinkan URL. Untuk menolaknya, raise `ToolError` (throw di TypeScript). Claude membaca pesan error tersebut, dan `navigate` tidak berjalan. Kebijakan hanya memeriksa URL dalam setiap panggilan `navigate`. Kebijakan ini bukan kontrol jaringan.

Ini adalah kebijakan dari mulai cepat. Kebijakan ini mengizinkan `about:blank`, ditambah dua situs dan subdomainnya melalui `http` dan `https`:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  import re
  from urllib.parse import urlsplit

  from anthropic.tools import ToolError
  from anthropic.tools.browser import BetaURLContext

  ALLOWED_HOSTS = ("example.com", "iana.org")
  SCHEME_PREFIX = re.compile(r"[a-z][a-z0-9+.-]*:", re.IGNORECASE)


  def is_allowed(url: str) -> bool:
      # Sebuah contoh, bukan kebijakan produksi.
      if url.lower() == "about:blank":
          return True
      with_scheme = url if SCHEME_PREFIX.match(url) else f"https://{url}"
      # Browser membaca "\" sebagai "/" dalam URL web.
      try:
          parts = urlsplit(with_scheme.replace("\\", "/"))
      except ValueError:
          return False
      host = parts.hostname or ""
      listed = any(host == name or host.endswith(f".{name}") for name in ALLOWED_HOSTS)
      return parts.scheme in ("http", "https") and listed


  def url_policy(context: BetaURLContext, url: str) -> None:
      if not is_allowed(url):
          raise ToolError(f"blocked: {url} is not on an allowed host")


  browser = MyBrowser(backend, url_policy=url_policy)
  ```

  ```typescript TypeScript
  import { type BetaURLContext, ToolError } from "@anthropic-ai/sdk/helpers/beta/toolsets";

  const ALLOWED_HOSTS = ["example.com", "iana.org"];
  const SCHEME_PREFIX = /^[a-z][a-z0-9+.-]*:/i;

  // Sebuah contoh, bukan kebijakan produksi.
  function isAllowed(url: string): boolean {
    if (url.toLowerCase() === "about:blank") return true;
    const withScheme = SCHEME_PREFIX.test(url) ? url : `https://${url}`;
    // Browser membaca "\" sebagai "/" dalam URL web.
    const parsed = URL.parse(withScheme.replaceAll("\\", "/"));
    const host = parsed?.hostname ?? "";
    const listed = ALLOWED_HOSTS.some((name) => host === name || host.endsWith(`.${name}`));
    return (parsed?.protocol === "http:" || parsed?.protocol === "https:") && listed;
  }

  function urlPolicy(ctx: BetaURLContext, url: string): void {
    if (!isAllowed(url)) throw new ToolError(`blocked: ${url} is not on an allowed host`);
  }

  const browser = new MyBrowser(backend, { urlPolicy });
  ```
</CodeGroup>

SDK memanggil kebijakan hanya untuk `navigate`, dan tidak untuk `"back"`, `"forward"`, atau `"reload"`. Claude dapat menghilangkan skema, seperti pada `example.com`, sehingga sebelum membaca host, contoh ini menambahkan `https://` ke URL yang tidak diawali skema. `navigate` Anda menerima URL sebagaimana ditulis Claude. Tambahkan skema di sana dengan pengujian yang sama, sehingga browser membuka URL yang diperiksa oleh kebijakan Anda.

Contoh ini tidak berkualitas produksi. Kebijakan produksi membutuhkan jauh lebih banyak, di area seperti berikut:

* Tautan yang diklik Claude, formulir yang dikirimkannya, redirect, dan request yang dibuat halaman dengan sendirinya. Hanya driver Anda yang melihatnya. Lihat [Mengintersep permintaan di driver](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#intercept-requests-in-the-driver).
* Hostname dan URL yang berasal dari konten halaman, yang dapat dipilih oleh penyerang.
* Mem-parse setiap URL seperti yang dilakukan browser, bukan menemukan hostname dengan pemisahan string biasa.
* Skema URL. SDK tidak memeriksanya, jadi tolak setiap skema yang tidak dimaksudkan untuk dibuka oleh driver Anda.
* Aturan egress pada container, untuk apa yang tidak dapat dilihat oleh pemeriksaan URL mana pun. Lihat [Menerapkan kebijakan egress pada container](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#put-egress-policy-on-the-container).

Jika Anda memberikan `url_policy=None` (typescript: `urlPolicy: null`), SDK menolak setiap `navigate` ke sebuah URL, sehingga `None` (typescript: `null`) yang dibaca dari konfigurasi Anda tidak dapat secara tidak sengaja membiarkan URL tidak diperiksa. Di TypeScript, `undefined` membiarkan opsi tidak diatur, sama seperti tidak memberikannya.

### Mengintersep permintaan di driver

Kebijakan URL hanya menilai URL dalam panggilan `navigate`. Tautan yang diklik Claude, formulir yang dikirimkannya, redirect, atau gambar atau skrip pada halaman yang diizinkan masih dapat menjangkau host yang akan ditolak oleh kebijakan. Gunakan [aturan egress](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#put-egress-policy-on-the-container) untuk memblokir host tersebut.

Driver dengan intersepsi request juga dapat memeriksa request tersebut di request hook-nya, yaitu fungsi yang dipanggil pustaka otomatisasi Anda sebelum setiap request. Panggil fungsi yang digunakan kebijakan Anda, sehingga Anda menulis aturannya sekali saja:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  class MyBrowser(BetaAbstractBrowserToolset20260801):
      ...

      # Didaftarkan pada konteks browser Playwright dengan context.route("**/*", self._guard)
      def _guard(self, route):
          # is_allowed adalah fungsi dari "Write a URL policy"
          if not is_allowed(route.request.url):
              return route.abort("blockedbyclient")
          route.continue_()
  ```

  ```typescript TypeScript
  // Di kelas driver, pada konteks browser Playwright.
  // isAllowed adalah fungsi dari "Write a URL policy".
  await context.route("**/*", (route) =>
    isAllowed(route.request().url()) ? route.continue() : route.abort("blockedbyclient")
  );
  ```
</CodeGroup>

Request hook seperti ini tidak melihat handshake WebSocket, request service-worker, atau lompatan redirect. Blokir service worker. Periksa handshake WebSocket dan lompatan redirect dengan hook yang dapat melihatnya. Contoh kebijakan menolak URL `ws://` dan `wss://`, jadi ubah `ws://` menjadi `http://` dan `wss://` menjadi `https://` sebelum Anda memberikan URL WebSocket ke `is_allowed` (typescript: `isAllowed`).

### Menerapkan kebijakan egress pada container

Intersepsi tidak dapat melihat setiap permintaan yang dibuat browser, dan kebijakan URL tidak melihat ke mana suatu nama di-resolve. Kebijakan "egress" (lalu lintas keluar) yang ditegakkan oleh jaringan container mencakup keduanya:

* Blokir rentang alamat link-local dan privat di IPv4 dan IPv6. Itu termasuk alamat metadata cloud `169.254.169.254`.
* Izinkan koneksi keluar hanya ke host yang dibutuhkan tugas. Jika aturan Anda mencocokkan alamat IP, resolve hostname yang Anda izinkan saat container dimulai.
* Izinkan DNS hanya ke resolver container.

Aturan yang diterapkan di luar container browser, seperti Kubernetes NetworkPolicy atau firewall cloud, tidak melihat loopback di dalamnya. Dengan hanya aturan tersebut, sebuah halaman dapat menjangkau apa pun yang mendengarkan di sana, termasuk port DevTools, yang menampilkan daftar tab browser yang terbuka dan alamat yang mengendalikan masing-masing tab.

### Membatasi unggahan dan unduhan

`file_upload` nonaktif secara default. Tanpa `file_policy` (typescript: `filePolicy`), SDK menolak setiap unggahan yang menyebutkan path atau [ID dokumen](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool#upload-files). Untuk mengaktifkan unggahan, berikan `BetaLocalFilePolicy` (typescript: `BetaNodeFilePolicy`) dengan satu direktori unggahan yang hanya berisi file tugas:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  from anthropic.tools.browser import BetaLocalFilePolicy

  # MyBrowser yang juga mengimplementasikan file_upload
  browser = MyBrowser(
      backend,
      configs={"file_upload": {"enabled": True}},
      confirm=make_confirm(),  # required for file_upload; see Gate consequential members
      url_policy=url_policy,
      file_policy=BetaLocalFilePolicy(
          upload_roots=["/task/uploads"],
          download_dir="/task/downloads",
          expose_download_paths=False,
      ),
  )
  ```

  ```typescript TypeScript
  import { BetaNodeFilePolicy } from "@anthropic-ai/sdk/helpers/beta/toolsets/node";

  // MyBrowser yang juga mengimplementasikan file_upload
  const browser = new MyBrowser(backend, {
    configs: { file_upload: { enabled: true } },
    confirm: makeConfirm(), // required for file_upload; see Gate consequential members
    urlPolicy,
    filePolicy: new BetaNodeFilePolicy({
      uploadRoots: ["/task/uploads"],
      downloadDir: "/task/downloads",
      exposeDownloadPaths: false
    })
  });
  ```
</CodeGroup>

SDK me-resolve setiap path unggahan, mengikuti symlink, dan menolak path apa pun di luar root unggahan. Kebijakan file me-raise error konfigurasi untuk direktori unduhan yang merupakan root unggahan, berada di dalamnya, atau berisi root unggahan. Pemeriksaan itu dapat melewatkan symlink, jadi jangan biarkan symlink membuat direktori unduhan sama dengan root unggahan, atau menempatkan salah satunya di dalam yang lain. SDK menyertakan `path` unduhan dalam laporan status hanya ketika `expose_download_paths` (typescript: `exposeDownloadPaths`) bernilai true dan file berada di dalam direktori unduhan.

Kebijakan file bawaan memeriksa path pada filesystem proses yang menjalankan SDK. Kebijakan ini hanya melindungi browser yang berbagi filesystem tersebut. Untuk browser remote, ikuti [Browser remote dan hosted](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#remote-and-hosted-browsers) sebagai gantinya.

Siapkan unduhan dengan cara berikut:

* Buat direktori unduhan sendiri dengan mode `0700`, dan mount dengan `noexec,nosuid,nodev`.
* Jauhkan direktori tersebut dari jangkauan alat lain yang dapat dipanggil Claude, seperti shell atau alat file.
* Dalam perubahan state `download_failed`, tulis `error` sebagai frasa tetap. Teks exception dapat berisi path atau URL.
* Jangan membaca file yang diunduh ke dalam percakapan, atau menjalankannya, sampai seseorang memutuskan untuk melakukannya.

### Membatasi anggota yang berdampak

`javascript_exec` dan `file_upload` nonaktif secara default. Jika Anda mengaktifkan salah satunya tanpa callable `confirm`, constructor me-raise error konfigurasi. Dengan callable `confirm`, SDK memanggilnya sebelum setiap panggilan yang akan berjalan. Tanpanya, tidak ada yang ditanyakan. Di TypeScript, `confirm: null` tidak me-raise error konfigurasi, dan SDK menolak setiap panggilan ke anggota mana pun.

Kembalikan `True` (typescript: `true`) untuk menjalankan panggilan, atau `False` (typescript: `false`) untuk menolaknya. Ketika callable Anda bertanya kepada seseorang, tunjukkan anggota, URL halaman, dan input panggilan. Pertama, escape setiap karakter di luar ASCII yang dapat dicetak dalam URL dan input, karena keduanya dapat membawa teks dari halaman.

Contoh ini menanyakan tentang dua anggota yang dilindungi melalui fungsi `ask_user` (typescript: `askUser`) Anda sendiri, dan menyetujui sisanya:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  import json
  from collections.abc import Callable
  from urllib.parse import urlsplit

  from anthropic.tools.browser import BetaConfirmContext

  GATED = {"javascript_exec", "file_upload"}


  def shown(value: object) -> str:
      """A value as JSON, with every character outside printable ASCII escaped."""
      return json.dumps(value, ensure_ascii=True, indent=2)


  def make_confirm() -> Callable[[BetaConfirmContext], bool]:
      granted: set[tuple[str, str, str]] = set()

      def confirm(context: BetaConfirmContext) -> bool:
          name = context.member
          if name not in GATED:
              return True
          detail = shown(context.input.to_dict())
          page = context.tab_url
          where = shown(page) if page else "a tab with no URL"
          question = f"Allow {name} on {where}?\n{detail}"
          if page is None or urlsplit(page).scheme not in ("http", "https"):
              return ask_user(question)  # no web origin: ask every time
          # Persetujuan hanya berlaku untuk input persis ini di halaman ini.
          key = (name, page, detail)
          if key not in granted and ask_user(question):
              granted.add(key)
          return key in granted

      return confirm


  # MyBrowser yang juga mengimplementasikan javascript_exec dan file_upload
  # file_upload juga memerlukan file_policy dari "Confine uploads and downloads"
  browser = MyBrowser(
      backend,
      configs={"javascript_exec": {"enabled": True}, "file_upload": {"enabled": True}},
      confirm=make_confirm(),
      url_policy=url_policy,
  )
  ```

  ```typescript TypeScript
  import type { BetaConfirmContext } from "@anthropic-ai/sdk/helpers/beta/toolsets";

  const GATED = new Set(["javascript_exec", "file_upload"]);

  /** A value as JSON, with every character outside printable ASCII escaped. */
  const shown = (value: unknown): string =>
    JSON.stringify(value, null, 2).replace(
      /[^\n\x20-\x7e]/g,
      (match) => `\\u${match.charCodeAt(0).toString(16).padStart(4, "0")}`
    );

  const makeConfirm = () => {
    const granted = new Set<string>();
    return async (ctx: BetaConfirmContext): Promise<boolean> => {
      const name = ctx.member;
      if (!GATED.has(name)) return true;
      const detail = shown(ctx.input);
      const page = ctx.tabURL;
      const where = page ? shown(page) : "a tab with no URL";
      const question = `Allow ${name} on ${where}?\n${detail}`;
      const scheme = page === undefined ? undefined : URL.parse(page)?.protocol;
      if (scheme !== "http:" && scheme !== "https:") {
        return askUser(question); // no web origin: ask every time
      }
      // Persetujuan hanya berlaku untuk input persis ini di halaman ini.
      const key = `${name} ${page} ${detail}`;
      if (!granted.has(key) && (await askUser(question))) {
        granted.add(key);
      }
      return granted.has(key);
    };
  };

  // MyBrowser yang juga mengimplementasikan javascript_exec dan file_upload
  // file_upload juga memerlukan filePolicy dari "Confine uploads and downloads"
  const browser = new MyBrowser(backend, {
    configs: { javascript_exec: { enabled: true }, file_upload: { enabled: true } },
    confirm: makeConfirm(),
    urlPolicy
  });
  ```
</CodeGroup>

Setiap panggilan ke `make_confirm()` (typescript: `makeConfirm()`) mengembalikan callable tanpa persetujuan. Panggil sekali untuk setiap toolset, dan berikan setiap pengguna toolset mereka sendiri.

Persetujuan mencakup halaman sebagaimana ditunjukkan oleh laporan state terakhir, dan halaman dapat berubah sebelum panggilan berjalan. Pembelian, pesan yang dikirim, dan persyaratan yang diterima terjadi melalui anggota biasa seperti `left_click` dan `type`, sehingga `confirm` tidak dapat memilahnya berdasarkan nama. Agar seseorang menyetujui tindakan tersebut, tanyakan juga tentang anggota-anggota itu.

Jangan aktifkan `javascript_exec` kecuali [aturan egress](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#put-egress-policy-on-the-container) membatasi koneksi keluar browser ke host yang dibutuhkan tugas. Sebuah skrip dapat mengirim konten halaman ke alamat mana pun yang dapat dijangkau browser.

URL `javascript:` dalam panggilan `navigate` juga menjalankan skrip di halaman saat ini, bahkan ketika `javascript_exec` nonaktif. `confirm` melihat panggilan itu sebagai `navigate`, sehingga callable `confirm` dalam contoh akan menyetujuinya. Driver Anda harus menolak URL `javascript:`. Dalam contoh, [kebijakan URL](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#write-a-url-policy) menolaknya sebelum `confirm` berjalan.

### Mengisolasi host browser

Jalankan browser dalam container atau VM khusus dengan hak akses minimal untuk setiap sesi:

* Jalankan sebagai pengguna non-root, dengan filesystem root read-only jika browser mengizinkannya.
* Jangan mount apa pun dari host selain direktori unggahan dan unduhan yang Anda konfigurasikan, jika ada.
* Jauhkan kredensial dari lingkungan, dan mulai dari profil browser yang baru.
* Jangan berbagi filesystem dengan alat lain yang dapat dipanggil Claude.

<Warning>
  Profil browser tidak boleh masuk (signed in) ke akun mana pun yang data atau tindakannya tidak akan Anda serahkan kepada Claude. `javascript_exec` berjalan dengan otoritas halaman itu sendiri: cookie-nya, penyimpanannya, dan sesi masuknya.
</Warning>

Jalankan kode yang memanggil API di luar container browser, karena kode tersebut menyimpan kunci API Anda dan percakapan. Tool runner dan `tool_result` (typescript: `toolResult`) keduanya menjalankan toolset dalam proses kode tersebut, sehingga browser tidak berbagi filesystem toolset. Perlakukan browser sebagai remote: [Browser remote dan hosted](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#remote-and-hosted-browsers) berlaku.

Perlakukan semua yang dikembalikan halaman sebagai tidak tepercaya, termasuk teks halaman, screenshot, entri konsol dan jaringan, judul tab, dan nama unduhan.

### Browser remote dan hosted

Beberapa browser tidak berbagi filesystem dengan proses yang menjalankan SDK. Contohnya adalah browser di container lain, browser yang Anda jangkau melalui URL DevTools, dan browser dari layanan browser hosted. Dengan browser-browser ini, kebijakan URL, intersepsi permintaan, dan `confirm` tetap berjalan di proses Anda.

Dengan browser hosted, penyedia mengontrol egress dan isolasi host. Kebijakan egress Anda sendiri tidak berlaku di sana, sehingga hook permintaan driver adalah satu-satunya pemeriksaan Anda atas permintaan browser. Cari tahu apa saja yang dapat dijangkau oleh jaringan browser tersebut.

Pemeriksaan path bawaan tidak melindungi browser remote. `BetaLocalFilePolicy` (typescript: `BetaNodeFilePolicy`) memeriksa path pada filesystem proses yang menjalankan SDK, sedangkan browser membaca dan menulis filesystem-nya sendiri.

SDK tidak dapat mendeteksi bahwa sebuah browser bersifat remote. Jadi untuk browser remote, biarkan `file_upload` nonaktif kecuali driver Anda memeriksa path unggahan di tempat browser berjalan, dengan `BetaFilePolicy` miliknya sendiri. `BetaFilePolicy` memeriksa path dan ID dokumen setiap unggahan, dan memutuskan apakah Claude melihat path unduhan.

Buat browser remote menolak unduhan, kecuali host-nya sendiri memiliki penyiapan unduhan dari [Membatasi unggahan dan unduhan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#confine-uploads-and-downloads).

Jauhkan kunci API penyedia dan URL koneksi sesi, yang dapat berisi kunci, dari log, hasil alat, dan teks error. Jika penyedia merekam sesi, rekaman tersebut merupakan salinan lain dari semua yang dilihat dan diketik Claude, dan ketentuan retensi penyedia berlaku untuknya.

## Computer toolset

`BetaAbstractComputerToolset20260801` adalah kelas untuk [alat penggunaan komputer](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool). Anda membuat subclass darinya dan menulis satu metode per alat, seperti `screenshot` atau `left_click`, terhadap otomatisasi desktop Anda sendiri. Subclass Anda adalah driver-nya. SDK tidak menyertakan desktop atau driver siap pakai. [Contoh VNC minimal](https://github.com/anthropics/claude-quickstarts/tree/main/computer-toolset) ada di repositori claude-quickstarts, dalam Python dan TypeScript. Contoh ini mengendalikan desktop melalui VNC, dan bukan kode produksi.

Kelas ini menerima `configs`, `confirm`, dan `tool_configs` (typescript: `toolConfigs`), dan Anda memberikannya seperti pada kelas browser. [Menyesuaikan driver](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#customize-a-driver), [Menangani error](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#handle-errors), [Memulai panggilan saat respons sedang di-streaming](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#start-calls-while-the-response-streams), dan [Menjalankan tanpa tool runner](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#run-without-the-tool-runner) juga berlaku untuknya, dengan perbedaan berikut:

* **Opsi khusus browser:** Kelas ini tidak memiliki [kebijakan URL](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#write-a-url-policy), [kebijakan file](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#confine-uploads-and-downloads), maupun [laporan status](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#report-browser-state).
* **`configs`:** Setiap alat yang Anda implementasikan aktif secara default. Pengaturan per alat tercantum di [Parameter alat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#tool-parameters).
* **`confirm`:** Jika kelas Anda mengimplementasikan `type`, `key`, atau `hold_key`, constructor me-raise error konfigurasi kecuali Anda memberikan callable `confirm` atau menonaktifkan alat tersebut dengan `configs`. Kelas yang meng-override `execute` dianggap mengimplementasikan ketiganya.
* **Panggilan yang dilewati:** Setelah panggilan komputer gagal, tool runner menjawab panggilan komputer berikutnya dalam giliran tersebut dengan `Not executed: an earlier computer action in this turn failed.` Panggilan browser mendapat teks yang berbeda. Dalam loop yang Anda tulis, jawab panggilan komputer yang dilewati dengan teks persis tersebut ([Aksi batch](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#batch-actions)).
* **`execute`:** Di TypeScript, override `execute` memberi tipe `name` sebagai `BetaComputerMemberName` dan `input` sebagai `BetaComputerMemberInput`. Keduanya berasal dari `@anthropic-ai/sdk/resources/beta`.
* **Teks error:** SDK tidak menyembunyikan path lokal dalam teks error alat komputer atau dalam teks yang dikembalikan alat. Claude membaca keduanya, dipotong pada 4.096 karakter. Tangkap exception di alat Anda, dan raise `ToolError` (throw di TypeScript) dengan teks Anda sendiri.

### Menulis driver desktop

Driver ini mengimplementasikan lima dari 17 alat yang tercantum di [Tindakan yang tersedia](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#available-actions). Alat yang tidak Anda implementasikan dikirim ke API sebagai dinonaktifkan, seperti yang dijelaskan [Mulai cepat](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#quick-start). Dalam contoh, `display` mewakili wrapper Anda sendiri di sekitar apa pun yang mengendalikan desktop, seperti klien VNC atau `xdotool`, dan `ask_user` (typescript: `askUser`) mewakili fungsi Anda sendiri yang bertanya kepada seseorang.

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  from anthropic import Anthropic
  from anthropic.tools.computer import (
      BetaAbstractComputerToolset20260801,
      BetaComputerCursorPositionResult,
      BetaScreenshotResult,
      BetaToolsetCallContext,
  )
  from anthropic.types.beta import (
      BetaComputerCursorPositionInput,
      BetaComputerKeyInput,
      BetaComputerLeftClickInput,
      BetaComputerScreenshotInput,
      BetaComputerTypeInput,
  )


  class MyDesktop(BetaAbstractComputerToolset20260801):
      def __init__(self, display, **options):
          super().__init__(**options)
          self.display = display

      def screenshot(
          self, context: BetaToolsetCallContext, input: BetaComputerScreenshotInput
      ) -> BetaScreenshotResult:
          # Koordinat Claude adalah posisi piksel dalam gambar ini.
          data = self.display.png_base64()
          return BetaScreenshotResult(data=data, media_type="image/png")

      def cursor_position(
          self, context: BetaToolsetCallContext, input: BetaComputerCursorPositionInput
      ) -> BetaComputerCursorPositionResult:
          x, y = self.display.cursor()
          return BetaComputerCursorPositionResult(x=x, y=y)

      def left_click(
          self, context: BetaToolsetCallContext, input: BetaComputerLeftClickInput
      ) -> None:
          # input.coordinate berupa [x, y], atau None untuk mengklik di posisi kursor. input.text adalah
          # tombol pengubah yang ditahan, misalnya "shift". Tidak ada nilai kembalian: Claude membaca "Clicked."
          self.display.click(input.coordinate, input.text)

      def type(
          self, context: BetaToolsetCallContext, input: BetaComputerTypeInput
      ) -> None:
          self.display.type(input.text)

      def key(self, context: BetaToolsetCallContext, input: BetaComputerKeyInput) -> None:
          self.display.press(input.text, input.repeat or 1)

      def close(self) -> None:
          super().close()  # first, so no call is still using the desktop when it closes
          self.display.close()


  client = Anthropic()
  with MyDesktop(
      display,
      # wajib untuk type dan key; lihat Menjalankan toolset komputer dengan aman
      confirm=lambda context: ask_user(f'Allow the "{context.member}" tool?'),
  ) as desktop:
      runner = client.beta.messages.tool_runner(
          model="claude-opus-5-5",
          max_tokens=1024,
          tools=[desktop],
          messages=[
              {"role": "user", "content": "Open the calculator and compute 17 * 23."}
          ],
      )
      for message in runner:
          print(message)
  ```

  ```typescript TypeScript
  import Anthropic from "@anthropic-ai/sdk";
  import {
    BetaAbstractComputerToolset20260801,
    type BetaComputerCursorPositionResult,
    type BetaComputerToolsetOptions,
    type BetaScreenshotResult,
    type BetaToolsetCallContext
  } from "@anthropic-ai/sdk/helpers/beta/toolsets";
  import type {
    BetaComputerCursorPositionInput,
    BetaComputerKeyInput,
    BetaComputerLeftClickInput,
    BetaComputerScreenshotInput,
    BetaComputerTypeInput
  } from "@anthropic-ai/sdk/resources/beta";

  class MyDesktop extends BetaAbstractComputerToolset20260801 {
    constructor(private display: Display, options: BetaComputerToolsetOptions = {}) {
      super(options);
    }

    protected override async screenshot(
      ctx: BetaToolsetCallContext,
      input: BetaComputerScreenshotInput
    ): Promise<BetaScreenshotResult> {
      // Koordinat Claude adalah posisi piksel dalam gambar ini.
      return { data: await this.display.pngBase64(), mediaType: "image/png" };
    }

    protected override async cursor_position(
      ctx: BetaToolsetCallContext,
      input: BetaComputerCursorPositionInput
    ): Promise<BetaComputerCursorPositionResult> {
      const { x, y } = await this.display.cursor();
      return { x, y };
    }

    protected override async left_click(
      ctx: BetaToolsetCallContext,
      input: BetaComputerLeftClickInput
    ): Promise<void> {
      // input.coordinate berupa [x, y], atau null atau undefined untuk klik di posisi kursor. input.text
      // adalah tombol pengubah yang ditahan, seperti "shift". Tidak ada yang dikembalikan: Claude membaca "Clicked."
      await this.display.click(input.coordinate, input.text);
    }

    // Alat type ditulis sebagai type_ di TypeScript.
    protected override async type_(
      ctx: BetaToolsetCallContext,
      input: BetaComputerTypeInput
    ): Promise<void> {
      await this.display.type(input.text);
    }

    protected override async key(
      ctx: BetaToolsetCallContext,
      input: BetaComputerKeyInput
    ): Promise<void> {
      await this.display.press(input.text, input.repeat ?? 1);
    }

    override async close(): Promise<void> {
      await super.close(); // first, so no call is still using the desktop when it closes
      await this.display.close();
    }
  }

  const client = new Anthropic();
  const desktop = new MyDesktop(display, {
    // wajib untuk type dan key; lihat Menjalankan toolset komputer dengan aman
    confirm: (ctx) => askUser(`Allow the "${ctx.member}" tool?`)
  });
  try {
    const runner = client.beta.messages.toolRunner({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      tools: [desktop],
      messages: [{ role: "user", content: "Open the calculator and compute 17 * 23." }]
    });
    for await (const message of runner) console.log(message);
  } finally {
    await desktop.close();
  }
  ```
</CodeGroup>

<Warning>
  `confirm` dalam contoh ini bertanya kepada seseorang sebelum setiap panggilan yang dijalankan driver. Sebelum Anda menjalankan driver terhadap apa pun selain mesin sekali pakai, baca [Menjalankan computer toolset dengan aman](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#run-the-computer-toolset-safely).
</Warning>

Empat alat tidak memiliki field input: `screenshot`, `cursor_position`, `left_mouse_down`, dan `left_mouse_up`. Setiap tipe input, termasuk milik keempatnya, berasal dari `anthropic.types.beta` (typescript: `@anthropic-ai/sdk/resources/beta`).

Di TypeScript, tulis alat sebagai metode, bukan field arrow-function. [Mengimplementasikan driver](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#implement-a-driver) memberikan alasannya.

### Menskalakan koordinat dan mengatur ukuran gambar

Setiap titik yang dikirim Claude adalah posisi piksel dalam screenshot yang Anda kembalikan: setiap `coordinate` dan `start_coordinate`, serta kedua sudut dari `region` pada `zoom`. SDK meneruskannya ke alat Anda tanpa perubahan.

Jika screenshot Anda berukuran berbeda dari layar, lakukan konversi ke dua arah di driver Anda: titik dari Claude ke piksel layar, dan posisi kursor yang Anda laporkan ke piksel screenshot. Pertahankan ukuran screenshot yang sama selama seluruh sesi, dan berikan rasio aspek yang sama dengan layar:

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  from anthropic.tools import ToolError

  SCREENSHOT_SIZE = (1280, 720)  # the size of every full screenshot the driver returns
  DISPLAY_SIZE = (2560, 1440)


  def to_display(coordinate: list[int]) -> tuple[int, int]:
      x, y = coordinate
      width, height = SCREENSHOT_SIZE
      if not (0 <= x < width and 0 <= y < height):
          # Tolak titik tersebut. Memindahkannya ke dalam rentang akan mengklik lokasi yang tidak dipilih Claude.
          raise ToolError(f"[{x}, {y}] is outside the {width}x{height} screenshot")
      return x * DISPLAY_SIZE[0] // width, y * DISPLAY_SIZE[1] // height


  def to_screenshot(x: int, y: int) -> tuple[int, int]:
      width, height = DISPLAY_SIZE
      return x * SCREENSHOT_SIZE[0] // width, y * SCREENSHOT_SIZE[1] // height


  to_display([640, 360])  # (1280, 720)
  ```

  ```typescript TypeScript
  import { ToolError } from "@anthropic-ai/sdk/helpers/beta/toolsets";

  const SCREENSHOT_SIZE = { width: 1280, height: 720 }; // the size of every full screenshot
  const DISPLAY_SIZE = { width: 2560, height: 1440 };

  function toDisplay(coordinate: number[]): [number, number] {
    const [x, y] = coordinate;
    const { width, height } = SCREENSHOT_SIZE;
    if (x < 0 || x >= width || y < 0 || y >= height) {
      // Tolak titik tersebut. Memindahkannya ke dalam rentang akan mengklik lokasi yang tidak dipilih Claude.
      throw new ToolError(`[${x}, ${y}] is outside the ${width}x${height} screenshot`);
    }
    return [
      Math.floor((x * DISPLAY_SIZE.width) / width),
      Math.floor((y * DISPLAY_SIZE.height) / height)
    ];
  }

  function toScreenshot(x: number, y: number): [number, number] {
    return [
      Math.floor((x * SCREENSHOT_SIZE.width) / DISPLAY_SIZE.width),
      Math.floor((y * SCREENSHOT_SIZE.height) / DISPLAY_SIZE.height)
    ];
  }

  toDisplay([640, 360]); // [1280, 720]
  ```
</CodeGroup>

Panggil `to_display` (typescript: `toDisplay`) pada setiap `coordinate` dan `start_coordinate` sebelum Anda menindaklanjutinya, dan `to_screenshot` (typescript: `toScreenshot`) pada posisi yang dilaporkan oleh `cursor_position`. Klik atau scroll tanpa `coordinate` bertindak pada posisi kursor, sehingga tidak ada yang perlu dikonversi. Skalakan `region` pada `zoom` dengan faktor yang sama. Gambar `zoom` tidak mengubah hal ini: titik berikutnya yang dikirim Claude tetap merupakan posisi piksel dalam screenshot penuh.

SDK tidak pernah membaca atau mengubah ukuran gambar. API menolak gambar yang melebihi batas model, yang mengakhiri run. Skalakan setiap screenshot dan gambar `zoom` di driver. Lihat [Sesuaikan ukuran tangkapan layar agar sesuai batas gambar](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#handle-coordinate-scaling-for-higher-resolutions). Pada run yang panjang, satu permintaan dapat memuat lebih dari 20 gambar, dan API kemudian menerapkan batas yang lebih ketat pada setiap gambar. Lihat [Mengelola riwayat tangkapan layar](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#manage-screenshot-history).

### Pemeriksaan input dan hasil

Jangan mengandalkan SDK untuk memeriksa input suatu panggilan. Minta driver Anda memeriksa field yang digunakannya dan menolak panggilan yang tidak dapat dijalankannya: raise `ToolError` (throw di TypeScript). Claude membaca pesannya dan dapat mengirim panggilan yang sudah diperbaiki.

Kedua SDK tidak membatasi `duration`, jumlah `repeat`, maupun `scroll_amount`. Langkah 4 di bawah [Menjalankan computer toolset dengan aman](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#run-the-computer-toolset-safely) membahasnya.

Apa yang dikembalikan alat menentukan apa yang dibaca Claude:

| Alat                 | Mengembalikan                      | Yang dibaca Claude                                                                              |
| -------------------- | ---------------------------------- | ----------------------------------------------------------------------------------------------- |
| `screenshot`, `zoom` | `BetaScreenshotResult`             | Satu blok gambar                                                                                |
| `cursor_position`    | `BetaComputerCursorPositionResult` | `X={x},Y={y}`                                                                                   |
| Setiap alat lainnya  | Tidak ada, atau satu baris teks    | Konfirmasi singkat, seperti `Clicked.`, lalu baris yang dikembalikan dalam blok teks tersendiri |

### Menjalankan computer toolset dengan aman

Apa yang ada di layar mengarahkan tindakan Claude berikutnya. Sebuah halaman atau notifikasi dapat mencoba membuat Claude mengetik ke jendela yang salah, atau memicu tindakan dengan efek nyata.

<Warning>
  Driver yang mengimplementasikan `type`, `key`, atau `hold_key` memerlukan callable `confirm`. Tanpanya, konstruktor akan memunculkan error konfigurasi, kecuali `configs` menonaktifkan alat-alat tersebut. SDK sendiri tidak meminta persetujuan siapa pun: SDK menjalankan setiap panggilan yang disetujui oleh `confirm` Anda, dan tanpa `confirm` SDK menjalankan setiap panggilan, termasuk setiap klik. Setiap alat komputer yang Anda implementasikan aktif secara default.
</Warning>

Sebelum Anda menjalankan driver pada apa pun selain mesin sekali pakai, lakukan lima langkah berikut:

1. Isolasi desktop. Jalankan di container atau VM khusus dengan hak akses minimal untuk setiap sesi, tanpa kredensial dan tanpa mount host. Instal hanya aplikasi yang dibutuhkan tugas. Jalankan kode yang memanggil API di luarnya.
2. Batasi tindakan yang memiliki efek nyata dengan `confirm`. Pembelian atau pesan yang terkirim hanyalah `left_click`, `type`, atau `key` biasa, dan `confirm` menerima alat beserta inputnya, bukan layarnya. Jadi pilih alat mana yang memerlukan persetujuan berdasarkan aplikasi yang dapat dijangkau Claude di desktop.
3. Jauhkan terminal, dialog run, dan launcher dari desktop kecuali tugas membutuhkannya. Ketika salah satunya memiliki fokus keyboard, `type`, `key`, dan `hold_key` menjalankan apa pun yang diketik Claude, dan sebuah klik dapat memulai program. Jika tugas membutuhkannya, minta persetujuan seseorang sebelum input keyboard dan klik, dan isolasi desktop sehingga sebuah perintah tidak dapat menjangkau lebih jauh dari yang dibutuhkan tugas.
4. Tolak input yang tidak seharusnya dipenuhi desktop Anda, seperti titik di luar screenshot, `wait` selama beberapa menit, atau `repeat` atau `scroll_amount` yang sangat besar. Raise `ToolError` (throw di TypeScript) alih-alih memindahkan nilainya ke dalam rentang.
5. Perlakukan semua yang ada di layar sebagai tidak tepercaya, termasuk judul jendela dan teks clipboard. Jangan menjalankannya atau meneruskannya tanpa diperiksa.

SDK menerapkan langkah 2 melalui callable yang Anda berikan. Langkah-langkah lainnya bergantung pada driver dan deployment Anda. Tindakan pencegahan di bawah [Pertimbangan keamanan](https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool#security-considerations) juga berlaku.

`confirm` berikut meminta persetujuan seseorang sebelum input keyboard apa pun, melalui fungsi `ask_user` (typescript: `askUser`) milik Anda sendiri, dan menyetujui setiap panggilan lainnya. `context.member` (typescript: `ctx.member`) adalah nama alat. Agar seseorang juga menyetujui klik, atur `ASK_FIRST` ke `KEYBOARD | CLICKS` (typescript: `new Set([...KEYBOARD, ...CLICKS])`).

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  from anthropic.tools.computer import BetaComputerConfirmContext

  KEYBOARD = {"type", "key", "hold_key"}
  CLICKS = {
      "left_click",
      "right_click",
      "middle_click",
      "double_click",
      "triple_click",
      "left_click_drag",
      "left_mouse_down",
      "left_mouse_up",
  }
  ASK_FIRST = KEYBOARD


  def confirm(context: BetaComputerConfirmContext) -> bool:
      if context.member not in ASK_FIRST:
          return True
      # yang ditampilkan adalah fungsi dari "Gate consequential members".
      detail = shown(context.input.to_dict())
      return ask_user(f'Allow the "{context.member}" tool with this input?\n{detail}')


  desktop = MyDesktop(display, confirm=confirm)
  ```

  ```typescript TypeScript
  import type { BetaComputerConfirmContext } from "@anthropic-ai/sdk/helpers/beta/toolsets";

  const KEYBOARD = ["type", "key", "hold_key"];
  const CLICKS = [
    "left_click",
    "right_click",
    "middle_click",
    "double_click",
    "triple_click",
    "left_click_drag",
    "left_mouse_down",
    "left_mouse_up"
  ];
  const ASK_FIRST = new Set(KEYBOARD);

  async function confirm(ctx: BetaComputerConfirmContext): Promise<boolean> {
    if (!ASK_FIRST.has(ctx.member)) return true;
    // yang ditampilkan adalah fungsi dari "Gate consequential members".
    return askUser(`Allow the "${ctx.member}" tool with this input?\n${shown(ctx.input)}`);
  }

  const desktop = new MyDesktop(display, { confirm });
  ```
</CodeGroup>

Panggilan yang ditolak mendapatkan hasil error, dan run tetap berlanjut. Untuk panggilan `type` yang ditolak, Claude membaca `The user did not grant permission to run 'type'. Do not retry it unless the user asks you to.`

`confirm` ini menyetujui setiap alat yang tidak ada di `ASK_FIRST`, termasuk alat apa pun yang Anda tambahkan nanti. Untuk fail closed, setujui hanya alat yang tidak berpengaruh pada desktop (`screenshot`, `zoom`, `cursor_position`, dan `wait`) dan minta persetujuan untuk setiap alat lainnya.

### Menggunakan kedua toolset dalam satu permintaan

Berikan kedua instance di `tools`. Setiap panggilan membawa `toolset_name`-nya, `browser` atau `computer`, dan tool runner mengirim panggilan ke instance yang sesuai. Setelah panggilan gagal, tool runner hanya melewati panggilan berikutnya dalam giliran tersebut ke toolset yang sama, sehingga panggilan komputer yang gagal tidak melewati panggilan browser dalam giliran tersebut.

<CodeGroup exclude="shell:cURL, shell:CLI, csharp, go, java, php, ruby">
  ```python Python
  # MyBrowser, backend, dan url_policy berasal dari panduan mulai cepat.
  # confirm adalah fungsi dari "Run the computer toolset safely".
  with (
      MyBrowser(backend, url_policy=url_policy) as browser,
      MyDesktop(display, confirm=confirm) as desktop,
  ):
      runner = client.beta.messages.tool_runner(
          model="claude-opus-5-5",
          max_tokens=1024,
          tools=[browser, desktop],
          messages=[
              {
                  "role": "user",
                  "content": "Copy the heading on example.com into the open text editor.",
              }
          ],
          stream=True,
          run_tools_eagerly=True,  # so a call can start before the response ends
      )
      for stream in runner:
          print(stream.get_final_message())
  ```

  ```typescript TypeScript
  // MyBrowser, backend, dan urlPolicy berasal dari panduan mulai cepat.
  // confirm adalah fungsi dari "Run the computer toolset safely".
  const browser = new MyBrowser(backend, { urlPolicy });
  const desktop = new MyDesktop(display, { confirm });
  try {
    const runner = client.beta.messages.toolRunner({
      model: "claude-opus-5-5",
      max_tokens: 1024,
      tools: [browser, desktop],
      messages: [
        { role: "user", content: "Copy the heading on example.com into the open text editor." }
      ],
      stream: true,
      runToolsEagerly: true // so a call can start before the response ends
    });
    for await (const stream of runner) console.log(await stream.finalMessage());
  } finally {
    await Promise.all([browser.close(), desktop.close()]);
  }
  ```
</CodeGroup>

Dalam loop yang Anda tulis sendiri, jawab setiap panggilan dengan `tool_result` (typescript: `toolResult`) pada instance yang `toolset_name` (typescript: `toolsetName`)-nya cocok dengan `toolset_name` panggilan tersebut. Dalam setiap giliran, lacak panggilan yang gagal untuk setiap toolset secara terpisah, dan jawab panggilan yang dilewati dengan teks milik toolset tersebut. [Menjalankan tanpa tool runner](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#run-without-the-tool-runner) memuat teks untuk browser, dan poin Panggilan yang dilewati di bagian atas bagian ini memuat teks untuk computer.

## Referensi

Opsi konstruktor memiliki arti yang sama di kedua SDK:

| Python                  | TypeScript     | Mengatur                                                                       |
| ----------------------- | -------------- | ------------------------------------------------------------------------------ |
| `configs`               | `configs`      | Anggota mana yang diaktifkan                                                   |
| `confirm`               | `confirm`      | Callable yang menyetujui atau menolak setiap panggilan                         |
| `url_policy`            | `urlPolicy`    | Kebijakan URL Anda, yang dipanggil SDK sebelum setiap `navigate` ke sebuah URL |
| `file_policy`           | `filePolicy`   | Root unggahan dan eksposur path unduhan                                        |
| `tool_configs`          | `toolConfigs`  | Field untuk entri `tools`, seperti `cache_control`                             |
| Metode `_browser_state` | `browserState` | Laporan state                                                                  |

Kelas browser menerima setiap opsi dalam tabel. Kelas komputer menerima `configs`, `confirm`, dan `tool_configs` (typescript: `toolConfigs`).

Anda tidak dapat mengubah opsi setelah konstruksi. [Panduan browser toolset Python](https://github.com/anthropics/anthropic-sdk-python/blob/main/browser-toolset.md), [panduan browser toolset TypeScript](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/browser-toolset.md), [panduan computer toolset Python](https://github.com/anthropics/anthropic-sdk-python/blob/main/computer-toolset.md), dan [panduan computer toolset TypeScript](https://github.com/anthropics/anthropic-sdk-typescript/blob/main/computer-toolset.md) menjelaskan setiap opsi. Panduan Python juga membahas kelas async, `BetaAsyncAbstractBrowserToolset20260801` dan `BetaAsyncAbstractComputerToolset20260801`.

## Keterbatasan

* **Kebijakan URL hanya melihat panggilan `navigate`:** Kebijakan ini tidak melihat permintaan yang dibuat oleh halaman, atau halaman yang terbuka dengan cara lain, seperti dari tautan yang diklik Claude atau redirect. Lihat [Mengintersep permintaan di driver](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#intercept-requests-in-the-driver).
* **Persetujuan didasarkan pada laporan state terakhir:** Halaman dapat berubah setelah laporan tersebut. SDK tidak memeriksa ulang halaman sebelum panggilan berjalan.
* **Panggilan pada satu toolset berjalan satu per satu:** Anda tidak dapat menonaktifkan perilaku ini.
* **SDK tidak memeriksa apakah ID tab unik atau berapa banyak tab yang ada, dan tidak selalu memeriksa bahwa satu tab aktif:** API menolak laporan yang melanggar aturan tersebut.
* **Untuk panggilan komputer, `confirm` menerima alat beserta inputnya, bukan layarnya:** Anda tidak dapat mengetahui dari keduanya apa yang dilakukan klik pada titik tertentu.
* **SDK tidak mengubah ukuran gambar computer toolset:** API menolak gambar yang melebihi batas model. Lihat [Menskalakan koordinat dan mengatur ukuran gambar](https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-sdk#scale-coordinates-and-size-images).

## Langkah selanjutnya

<CardGroup cols={2}>
  <Card title="Alat penggunaan browser" icon="browser" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/browser-use-tool">
    Alat anggota, blok `browser_state`, dan pertimbangan keamanan alat tersebut.
  </Card>

  <Card title="Alat penggunaan komputer" icon="computer" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/computer-use-tool">
    17 alat, koordinat dan batas gambar, serta pertimbangan keamanan alat tersebut.
  </Card>

  <Card title="Tool runner (SDK)" icon="arrows-clockwise" href="https://platform.claude.com/docs/id/agents-and-tools/tool-use/tool-runner">
    Cara SDK menjalankan loop, dan cara mengubah pesan yang dikirimnya.
  </Card>

  <Card title="Memitigasi jailbreak dan injeksi prompt" icon="shield" href="https://platform.claude.com/docs/id/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks">
    Guardrail untuk aplikasi apa pun yang membaca konten tidak tepercaya.
  </Card>
</CardGroup>
