---
title: "C#でAnthropic Claude APIを叩く最小サンプル"
emoji: "💻"
type: "tech"
topics: ["csharp", "dotnet", "claude", "api", "ai"]
published: true
---

こんにちは。エンジニアをしている長井洸太です。

前回は「[Javaのコードレビューを生成AIに頼んだら何が返ってきたか](https://zenn.dev/kotajobs0/articles/2026-07-07-java-code-review-claude)」でJavaからClaudeを使う話を書きましたが、今回はC#側です。Anthropicは公式にPython・TypeScript向けSDKは出していますが、C#向けの公式SDKはありません。とはいえClaude APIは素のREST APIなので、`HttpClient` があればどの言語からでも叩けます。今回はNuGetパッケージなしで動く最小構成を整理します。

---

## 前提

- .NET 6以降（`HttpClient` と `System.Text.Json` は標準ライブラリに含まれる）
- Anthropicの APIキー（[console.anthropic.com](https://console.anthropic.com/) で発行）

追加パッケージは不要です。`System.Net.Http` と `System.Text.Json` だけで完結します。

---

## エンドポイントの形

Claude APIは `POST https://api.anthropic.com/v1/messages` にJSONを送るだけのシンプルな構成です。必須ヘッダーは3つ。

| ヘッダー | 値 |
|---------|-----|
| `x-api-key` | APIキー |
| `anthropic-version` | `2023-06-01` |
| `content-type` | `application/json` |

Javaの `HttpClient`（`java.net.http`）を使ったことがある人なら、構造はほぼ同じだと分かるはずです。

---

## 最小サンプルコード

```csharp
using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;

var apiKey = Environment.GetEnvironmentVariable("CLAUDE_API_KEY")
    ?? throw new InvalidOperationException("CLAUDE_API_KEY が設定されていません");

using var client = new HttpClient();
client.DefaultRequestHeaders.Add("x-api-key", apiKey);
client.DefaultRequestHeaders.Add("anthropic-version", "2023-06-01");

var requestBody = new
{
    model = "claude-haiku-4-5-20251001",
    max_tokens = 300,
    messages = new[]
    {
        new { role = "user", content = "C#の初心者に例外処理の基本を3行で説明して" }
    }
};

var json = JsonSerializer.Serialize(requestBody);
var content = new StringContent(json, Encoding.UTF8, "application/json");

var response = await client.PostAsync("https://api.anthropic.com/v1/messages", content);
response.EnsureSuccessStatusCode();

var responseBody = await response.Content.ReadAsStringAsync();
using var doc = JsonDocument.Parse(responseBody);

var text = doc.RootElement
    .GetProperty("content")[0]
    .GetProperty("text")
    .GetString();

Console.WriteLine(text);
```

匿名型でリクエストボディを組み立て、レスポンスは `JsonDocument` でパースしています。DTOクラスを定義してもいいのですが、最小サンプルとしてはこれで十分動きます。

---

## 実行結果

```
$ dotnet run
1. try-catchで例外が起きそうな処理を囲みます。
2. catchブロックで例外の種類ごとに処理を分岐できます。
3. finallyブロックはtryの結果に関わらず必ず実行されます。
```

---

## 気をつけたいポイント

### `EnsureSuccessStatusCode()` だけでは足りない

Claude APIはレート制限超過時に `429`、リクエスト不正時に `400` を返しますが、`EnsureSuccessStatusCode()` は例外を投げるだけでエラー内容までは教えてくれません。本番運用するなら、失敗時に `response.Content.ReadAsStringAsync()` でエラーボディを読んでログに残す処理を足す必要があります。

```csharp
if (!response.IsSuccessStatusCode)
{
    var error = await response.Content.ReadAsStringAsync();
    throw new HttpRequestException($"Claude API エラー: {response.StatusCode} {error}");
}
```

### `HttpClient` は使い回す

サンプルでは `using` で毎回破棄していますが、実際のアプリケーションでは `HttpClient` を都度生成するとソケットが枯渇する問題があります。`IHttpClientFactory` を使うか、`static readonly` で使い回すのがJava/C#どちらでも共通のセオリーです。

### タイムアウトはデフォルトより短めに

`HttpClient` のデフォルトタイムアウトは100秒です。長文生成でなければ、業務システムに組み込む場合は10〜30秒程度に短縮しておくと、API側の遅延がそのままシステム全体の応答遅延に直結するのを防げます。

```csharp
client.Timeout = TimeSpan.FromSeconds(20);
```

---

## まとめ

C#にはAnthropic公式SDKがない分、逆にHTTPリクエストの中身がそのまま見える形でClaude APIを触れました。ヘッダー3つとJSONボディだけの構成なので、社内のC#資産に組み込む際も特別なラッパーは不要です。

次回は、Javaのデザインパターンを生成AIと一緒に学ぶ話を書く予定です。

X（Twitter）で毎日ITセールスやAI活用の話を投稿しています。ぜひつながりましょう！

[@kotajobs0](https://x.com/kotajobs0)

---

*参考：Claude API公式ドキュメント https://docs.anthropic.com*
