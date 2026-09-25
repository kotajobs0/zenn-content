---
title: "【Wiki】HTTP通信・REST APIクライアント (Java/C# 実装リファレンス)"
emoji: "🛠️"
type: "tech"
topics: ["java", "csharp", "新人教育", "architecture", "wiki"]
published: true
---

## はじめに

チームメンバーの皆さん、リードエンジニアの[あなたの名前]です。

現代のアプリケーション開発において、HTTP通信、特にREST APIクライアントの実装は不可欠な技術要素です。外部サービスとの連携、マイクロサービス間の通信、フロントエンドからのデータ取得など、様々なシーンで利用されます。

本リファレンスは、チーム内で利用されるHTTP/REST APIクライアントの実装において、**品質、堅牢性、保守性、パフォーマンス**を確保するための技術標準を提供します。特に若手エンジニアの皆さんが「そのまま実行できる」コード例と共に、プロフェッショナルな視点での考慮事項を解説します。

このドキュメントを通して、以下のことを習得できます。

*   JavaおよびC#における最新のHTTPクライアントライブラリの利用方法
*   GET/POSTリクエストの基本的な実装とJSONボディの扱い
*   非同期処理、エラーハンドリングのベストプラクティス
*   メモリ効率、スレッドセーフ、適切なリソース管理といったプロフェッショナルな視点

### 対象読者
*   HTTP通信・REST APIクライアントの実装経験が浅いエンジニア
*   JavaまたはC#を用いてHTTPクライアントを実装する機会のある全てのエンジニア

---

## 1. HTTP通信とREST APIの基礎知識

まず、HTTP通信とREST APIの基本的な概念を簡単に復習しましょう。

### 1.1. HTTPメソッド

クライアントがサーバーに対してどのような操作を要求するかを示すものです。

*   **GET**: リソースの取得。副作用がないべき（冪等）。
*   **POST**: リソースの作成、または特定の処理の実行。
*   **PUT**: リソースの更新、または作成（指定したURIにリソースが存在しない場合）。冪等。
*   **PATCH**: リソースの部分更新。
*   **DELETE**: リソースの削除。冪等。

### 1.2. HTTPステータスコード

サーバーがクライアントのリクエストに対してどのような結果を返したかを示す3桁の数値です。

*   **2xx (成功)**:
    *   `200 OK`: リクエストが成功した。
    *   `201 Created`: リソースの作成に成功した。
    *   `204 No Content`: リクエストは成功したが、レスポンスボディがない。
*   **4xx (クライアントエラー)**:
    *   `400 Bad Request`: リクエストの構文が不正、またはパラメータが不正。
    *   `401 Unauthorized`: 認証が必要、または認証に失敗した。
    *   `403 Forbidden`: 認証済みだが、リソースへのアクセス権がない。
    *   `404 Not Found`: リソースが見つからない。
    *   `429 Too Many Requests`: 短時間に過剰なリクエストが行われた（レートリミット）。
*   **5xx (サーバーエラー)**:
    *   `500 Internal Server Error`: サーバー内部で予期せぬエラーが発生した。
    *   `502 Bad Gateway`: ゲートウェイまたはプロキシサーバーが不正なレスポンスを受け取った。
    *   `503 Service Unavailable`: サーバーが一時的に処理できない状態（メンテナンスなど）。

### 1.3. RESTの原則

REST (Representational State Transfer) は、分散システムを設計するためのアーキテクチャスタイルです。

*   **リソース指向**: 全ての情報はURIで識別される「リソース」として表現されます。
*   **ステートレス**: 各リクエストは独立しており、サーバーは過去のリクエストの状態を保持しません。セッション管理はクライアント側で行います。
*   **統一インターフェース**: HTTPメソッド（GET, POSTなど）を用いてリソースを操作します。
*   **クライアント-サーバー分離**: クライアントとサーバーは独立して進化できます。

---

## 2. JavaにおけるHTTP/REST APIクライアント実装

### 2.1. クライアントライブラリの歴史と選択

Javaには様々なHTTPクライアントが存在しますが、バージョンアップに伴い推奨されるものが変化しています。

*   **`java.net.HttpURLConnection`**: Javaの初期から存在する標準API。低レベルで使いこなすには多くのボイラープレートコードが必要です。
*   **Apache HttpClient**: 長らくデファクトスタンダードとして利用されてきたサードパーティライブラリ。高機能ですが、外部依存が増えます。
*   **`java.net.http.HttpClient` (Java 11+)**: Java 11で標準APIとして導入された新しいHTTPクライアント。非同期処理に最適化され、モダンなAPI設計が特徴です。

**本記事では、Java 11以降のプロジェクトでは `java.net.http.HttpClient` の利用を強く推奨します。**

### 2.2. `HttpClient` を用いた実装 (Java 11+)

#### 依存関係の追加 (JSON処理のため)

実プロジェクトでは、JSONデータのシリアライゼーション/デシリアライゼーションのために、[Jackson](https://github.com/FasterXML/jackson) や [Gson](https://github.com/google/gson) といったライブラリの利用を強く推奨します。ここではJacksonを例に、Maven/Gradleの依存関係を示します。

```xml
<!-- Maven (pom.xml) -->
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.15.2</version> <!-- 最新バージョンを適宜確認してください -->
</dependency>
```

```gradle
// Gradle (build.gradle)
implementation 'com.fasterxml.jackson.core:jackson-databind:2.15.2' // 最新バージョンを適宜確認してください
```

#### 2.2.1. 基本的なGETリクエスト

外部APIからデータを取得する最も基本的な例です。

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;

public class JavaHttpClientGetExample {

    // HttpClientインスタンスはスレッドセーフであり、リソース効率のため使い回しが推奨されます。
    // static final で定義するか、DIコンテナでシングルトンとして管理するのが一般的です。
    private static final HttpClient HTTP_CLIENT = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_2) // HTTP/2 を優先的に使用
            .connectTimeout(Duration.ofSeconds(10)) // 接続タイムアウト
            .build();

    public static void main(String[] args) {
        String url = "https://jsonplaceholder.typicode.com/posts/1"; // テスト用の公開API

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET() // GETリクエストを指定
                .header("Accept", "application/json") // レスポンス形式をJSONに指定
                .timeout(Duration.ofSeconds(20)) // リクエスト全体のタイムアウト
                .build();

        try {
            // 同期でリクエストを送信し、レスポンスを受信する
            HttpResponse<String> response = HTTP_CLIENT.send(request, HttpResponse.BodyHandlers.ofString());

            System.out.println("Status Code: " + response.statusCode());
            System.out.println("Response Body:\n" + response.body());

            // ステータスコードが2xx系か確認
            if (response.statusCode() >= 200 && response.statusCode() < 300) {
                System.out.println("GETリクエスト成功！");
            } else {
                System.err.println("GETリクエスト失敗: " + response.statusCode());
            }

        } catch (java.io.IOException e) {
            System.err.println("ネットワークまたはIOエラーが発生しました: " + e.getMessage());
            e.printStackTrace();
        } catch (java.lang.InterruptedException e) {
            // スレッドが中断された場合に発生
            System.err.println("リクエストが中断されました: " + e.getMessage());
            Thread.currentThread().interrupt(); // 中断状態を再設定
            e.printStackTrace();
        } catch (Exception e) {
            System.err.println("予期せぬエラーが発生しました: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

**解説:**

*   **`HttpClient.newBuilder().build()`**: `HttpClient` のインスタンスを生成します。設定を連鎖的に行えます。
    *   `version(HttpClient.Version.HTTP_2)`: 可能であればHTTP/2を使用するように指定します。パフォーマンス向上に寄与します。
    *   `connectTimeout(Duration.ofSeconds(10))`: サーバーへの接続確立にかかる最大時間を設定します。
*   **`HttpRequest.newBuilder().uri().GET().build()`**: `HttpRequest` のインスタンスを生成します。
    *   `uri(URI.create(url))`: リクエスト対象のURIを指定します。
    *   `GET()`: GETメソッドを指定します。`POST()`, `PUT()`, `DELETE()` なども同様に指定できます。
    *   `header("Accept", "application/json")`: レスポンスとしてJSON形式を希望することをサーバーに伝えます。
    *   `timeout(Duration.ofSeconds(20))`: リクエスト全体のタイムアウトを設定します。接続からレスポンスボディの読み込み完了までにかかる最大時間です。
*   **`HTTP_CLIENT.send(request, HttpResponse.BodyHandlers.ofString())`**: 同期的にリクエストを送信します。
    *   `HttpResponse.BodyHandlers.ofString()`: レスポンスボディを `String` として受け取るハンドラーを指定します。他にも `ofInputStream()`, `ofFile()`, `discarding()` などがあります。
*   **エラーハンドリング**: `IOException` (ネットワークやストリームエラー) と `InterruptedException` (スレッド中断) は特に適切に処理する必要があります。ステータスコードをチェックすることで、API側の論理的なエラーを判断できます。

#### 2.2.2. POSTリクエスト (JSONボディ)

JSONデータをサーバーに送信するPOSTリクエストの例です。

```java
import com.fasterxml.jackson.databind.ObjectMapper; // Jacksonを使用
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

public class JavaHttpClientPostExample {

    private static final HttpClient HTTP_CLIENT = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_2)
            .connectTimeout(Duration.ofSeconds(10))
            .build();

    // ObjectMapperはスレッドセーフかつ高コストなので、シングルトンとして使い回しが推奨されます。
    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    public static void main(String[] args) {
        String url = "https://jsonplaceholder.typicode.com/posts"; // テスト用の公開API

        // 送信するJSONデータの準備
        Map<String, Object> postData = new HashMap<>();
        postData.put("title", "foo");
        postData.put("body", "bar");
        postData.put("userId", 1);

        try {
            // MapをJSON文字列に変換
            String requestBody = OBJECT_MAPPER.writeValueAsString(postData);

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .POST(HttpRequest.BodyPublishers.ofString(requestBody)) // POSTリクエストとボディを指定
                    .header("Content-Type", "application/json") // リクエストボディの形式をJSONに指定
                    .header("Accept", "application/json")
                    .timeout(Duration.ofSeconds(20))
                    .build();

            HttpResponse<String> response = HTTP_CLIENT.send(request, HttpResponse.BodyHandlers.ofString());

            System.out.println("Status Code: " + response.statusCode());
            System.out.println("Response Body:\n" + response.body());

            if (response.statusCode() >= 200 && response.statusCode() < 300) {
                System.out.println("POSTリクエスト成功！");
                // レスポンスボディをJavaオブジェクトにデシリアライズする例
                Map<String, Object> responseMap = OBJECT_MAPPER.readValue(response.body(), Map.class);
                System.out.println("Parsed Response: " + responseMap);
            } else {
                System.err.println("POSTリクエスト失敗: " + response.statusCode());
            }

        } catch (com.fasterxml.jackson.core.JsonProcessingException e) {
            System.err.println("JSON処理エラーが発生しました: " + e.getMessage());
            e.printStackTrace();
        } catch (java.io.IOException e) {
            System.err.println("ネットワークまたはIOエラーが発生しました: " + e.getMessage());
            e.printStackTrace();
        } catch (java.lang.InterruptedException e) {
            System.err.println("リクエストが中断されました: " + e.getMessage());
            Thread.currentThread().interrupt();
            e.printStackTrace();
        } catch (Exception e) {
            System.err.println("予期せぬエラーが発生しました: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
```

**解説:**

*   **`OBJECT_MAPPER.writeValueAsString(postData)`**: Jacksonの `ObjectMapper` を使用してJavaオブジェクトをJSON文字列に変換します。
*   **`POST(HttpRequest.BodyPublishers.ofString(requestBody))`**: POSTメソッドを指定し、リクエストボディをJSON文字列として設定します。他にもファイルやバイト配列を送信するための `BodyPublishers` が用意されています。
*   **`header("Content-Type", "application/json")`**: サーバーに対して、送信するリクエストボディがJSON形式であることを明示します。これは非常に重要です。

#### 2.2.3. 非同期処理 (`CompletableFuture`)

ブロッキングを避けて、バックグラウンドでHTTPリクエストを実行し、処理が完了したらコールバック関数を実行します。

```java
import com.fasterxml.jackson.databind.ObjectMapper;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;

public class JavaHttpClientAsyncExample {

    private static final HttpClient HTTP_CLIENT = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_2)
            .connectTimeout(Duration.ofSeconds(10))
            .build();

    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    public static void main(String[] args) {
        String getUrl = "https://jsonplaceholder.typicode.com/posts/2";
        String postUrl = "https://jsonplaceholder.typicode.com/posts";

        // 非同期GETリクエスト
        CompletableFuture<HttpResponse<String>> getFuture = sendAsyncGetRequest(getUrl);

        // 非同期POSTリクエスト
        Map<String, Object> postData = new HashMap<>();
        postData.put("title", "async foo");
        postData.put("body", "async bar");
        postData.put("userId", 2);
        CompletableFuture<HttpResponse<String>> postFuture = sendAsyncPostRequest(postUrl, postData);

        // 両方のリクエストが完了するのを待機し、結果を処理
        CompletableFuture.allOf(getFuture, postFuture)
                .thenRun(() -> {
                    System.out.println("--- All async requests completed ---");
                    try {
                        System.out.println("GET Response Status: " + getFuture.get().statusCode());
                        System.out.println("GET Response Body: " + getFuture.get().body().substring(0, Math.min(getFuture.get().body().length(), 100)) + "...");
                        
                        System.out.println("POST Response Status: " + postFuture.get().statusCode());
                        System.out.println("POST Response Body: " + postFuture.get().body().substring(0, Math.min(postFuture.get().body().length(), 100)) + "...");
                    } catch (InterruptedException | ExecutionException e) {
                        System.err.println("非同期処理の結果取得中にエラー: " + e.getMessage());
                    }
                })
                .exceptionally(ex -> {
                    System.err.println("非同期リクエスト中にエラーが発生しました: " + ex.getMessage());
                    return null;
                });

        System.out.println("メインスレッドは非同期リクエストの完了を待機中...");
        // 実際のアプリケーションでは、メインスレッドが終了しないように何らかの待機処理が必要です。
        // ここでは簡単な例として数秒待機。
        try {
            Thread.sleep(5000); // 5秒待機
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    private static CompletableFuture<HttpResponse<String>> sendAsyncGetRequest(String url) {
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .GET()
                .header("Accept", "application/json")
                .timeout(Duration.ofSeconds(20))
                .build();

        System.out.println("非同期GETリクエスト送信中: " + url);
        return HTTP_CLIENT.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                .thenApply(response -> {
                    System.out.println("非同期GETリクエスト完了 (Status: " + response.statusCode() + ")");
                    return response;
                })
                .exceptionally(e -> {
                    System.err.println("非同期GETリクエスト失敗: " + e.getMessage());
                    throw new RuntimeException("GET request failed", e);
                });
    }

    private static CompletableFuture<HttpResponse<String>> sendAsyncPostRequest(String url, Map<String, Object> data) {
        try {
            String requestBody = OBJECT_MAPPER.writeValueAsString(data);
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(url))
                    .POST(HttpRequest.BodyPublishers.ofString(requestBody))
                    .header("Content-Type", "application/json")
                    .header("Accept", "application/json")
                    .timeout(Duration.ofSeconds(20))
                    .build();

            System.out.println("非同期POSTリクエスト送信中: " + url);
            return HTTP_CLIENT.sendAsync(request, HttpResponse.BodyHandlers.ofString())
                    .thenApply(response -> {
                        System.out.println("非同期POSTリクエスト完了 (Status: " + response.statusCode() + ")");
                        return response;
                    })
                    .exceptionally(e -> {
                        System.err.println("非同期POSTリクエスト失敗: " + e.getMessage());
                        throw new RuntimeException("POST request failed", e);
                    });
        } catch (com.fasterxml.jackson.core.JsonProcessingException e) {
            System.err.println("JSON処理エラー (POST): " + e.getMessage());
            return CompletableFuture.failedFuture(e);
        }
    }
}
```

**解説:**

*   **`HTTP_CLIENT.sendAsync()`**: `CompletableFuture<HttpResponse<T>>` を返します。これは非同期処理の結果を表すオブジェクトです。
*   **`thenApply()` / `exceptionally()`**: `CompletableFuture` のメソッドチェーンを使用して、非同期処理が成功した場合（`thenApply`）や失敗した場合（`exceptionally`）のコールバック処理を定義します。
*   **`CompletableFuture.allOf()`**: 複数の `CompletableFuture` の完了を待ち、全てが完了したときに次の処理に進むことができます。
*   **メインスレッドのブロック**: 非同期処理は別スレッドで実行されるため、`main` メソッドがすぐに終了しないよう、`Thread.sleep()` や `future.get()` で待機する必要があります。`get()` はブロッキングメソッドであるため、使用は慎重に。非同期処理の全体的なフローを管理する際には、適切なフレームワークやExecutorServiceの利用を検討してください。

#### 2.2.4. プロフェッショナルな視点 (Java)

1.  **`HttpClient` インスタンスの再利用**:
    `HttpClient` の生成はリソースを消費するため、**アプリケーション内で単一のインスタンスを使い回す**ことを強く推奨します。`HttpClient` はスレッドセーフです。
    *   **シングルトンパターン**: アプリケーション全体で共有されるHTTPクライアントインスタンスを生成します。
    *   **DIコンテナ**: Spring FrameworkのようなDIコンテナを使用している場合、`HttpClient` をBeanとして定義し、シングルトンスコープで管理するのが最も一般的で推奨される方法です。
2.  **メモリ効率と大きなレスポンスボディ**:
    非常に大きなレスポンスボディを扱う場合、`HttpResponse.BodyHandlers.ofString()` で全てをメモリにロードするのは危険です。
    *   `HttpResponse.BodyHandlers.ofInputStream()`: レスポンスボディを `InputStream` として扱い、ストリーミング処理を行うことができます。これにより、メモリフットプリントを抑えられます。
    *   `HttpResponse.BodyHandlers.ofFile(Path file)`: レスポンスボディを直接ファイルに書き込むことができます。
3.  **適切なタイムアウト設定**:
    外部サービスへのHTTPリクエストは、ネットワークの遅延やサーバーの応答遅延により、アプリケーション全体のパフォーマンスボトルネックとなる可能性があります。
    *   `connectTimeout`: サーバーへの接続確立にかかる時間。
    *   `timeout`: リクエスト全体の完了にかかる時間（接続、データ送信、データ受信を含む）。
    これらを適切な値に設定し、無限に待機する状況を避けることで、リソース枯渇やシステムのハングアップを防ぎます。
4.  **JSONシリアライゼーション/デシリアライゼーション**:
    Jackson (`ObjectMapper`) や Gson は高機能でパフォーマンスも優れています。カスタムオブジェクトとのマッピングや、日付フォーマット、NULL値の扱いなど、柔軟な設定が可能です。
    *   `ObjectMapper` も `HttpClient` と同様にスレッドセーフであり、生成コストがかかるため、**シングルトンとして使い回す**のがベストプラクティスです。
5.  **例外処理のベストプラクティス**:
    *   ネットワーク障害 (`IOException`) やリクエスト中断 (`InterruptedException`) はアプリケーションの堅牢性のために適切にキャッチし、ロギングし、場合によってはリトライなどのリカバリ戦略を適用します。
    *   HTTPステータスコード (`4xx`, `5xx`) に基づくエラーは、業務ロジックの一部として処理する必要があります。
    *   `Thread.currentThread().interrupt()`: `InterruptedException` をキャッチした場合、スレッドの中断状態を再設定することで、後続のコードが中断を検知できるようにすることが重要です。
6.  **ロギング**:
    HTTPリクエスト/レスポンスの詳細なロギングは、デバッグや監視に不可欠です。本番環境では、機密情報（パスワード、個人情報など）をログに出力しないよう注意し、ログレベルを適切に設定してください。
7.  **テスト容易性**:
    HTTPクライアントを直接利用するコードは、外部依存が強く単体テストが難しくなりがちです。
    *   HTTPクライアントをラップするインターフェースを定義し、DIによって注入することで、テスト時にはそのインターフェースのモック/スタブ実装に差し替えられるように設計します。
    *   [WireMock](http://wiremock.org/) のようなツールを使って、モックサーバーを立てて統合テストを行うことも有効です。

---

## 3. C#におけるHTTP/REST APIクライアント実装

### 3.1. クライアントライブラリの歴史と選択

C# (.NET Framework / .NET Core) にも複数のHTTPクライアントが存在します。

*   **`System.Net.HttpWebRequest`**: .NET Framework時代に広く使われた低レベルなAPI。現代では推奨されません。
*   **`System.Net.Http.HttpClient`**: .NET Framework 4.5 および .NET Core で導入されたモダンなHTTPクライアント。非同期処理 (`async`/`await`) と相性が良く、非常に使いやすいです。

**本記事では、`.NET Core 2.1` 以降のプロジェクトでは `System.Net.Http.HttpClient` および `IHttpClientFactory` の利用を強く推奨します。**

### 3.2. `HttpClient` を用いた実装

#### 依存関係の追加 (JSON処理のため)

.NET Core 3.1 および .NET 5+ 以降では、`System.Text.Json` が標準のJSONライブラリとして組み込まれています。外部ライブラリを追加する必要は通常ありません。`.NET Standard 2.0` 以前のプロジェクトや、より複雑なJSON処理が必要な場合は `Newtonsoft.Json` を利用することもあります。

ここでは `System.Text.Json` を使用します。

#### 3.2.1. 基本的なGETリクエスト

外部APIからデータを取得する基本的な例です。

```csharp
using System;
using System.Net.Http;
using System.Threading.Tasks;

public class CSharpHttpClientGetExample
{
    // HttpClientインスタンスは適切に管理する必要があります。
    // 詳細については「プロフェッショナルな視点」セクションを参照してください。
    // この例ではシンプルに static インスタンスとしていますが、推奨されるパターンではありません。
    private static readonly HttpClient _httpClient = new HttpClient();

    public static async Task Main(string[] args)
    {
        string url = "https://jsonplaceholder.typicode.com/posts/1"; // テスト用の公開API

        try
        {
            // タイムアウト設定 (HttpClientインスタンス生成時に行うのが一般的)
            _httpClient.Timeout = TimeSpan.FromSeconds(20); 

            // Acceptヘッダーを設定
            _httpClient.DefaultRequestHeaders.Add("Accept", "application/json");

            // GETリクエストを非同期で送信
            HttpResponseMessage response = await _httpClient.GetAsync(url);

            Console.WriteLine($"Status Code: {(int)response.StatusCode} {response.StatusCode}");

            // ステータスコードが2xx系か確認
            response.EnsureSuccessStatusCode(); // 2xx以外の場合、HttpRequestExceptionをスロー

            string responseBody = await response.Content.ReadAsStringAsync();
            Console.WriteLine($"Response Body:\n{responseBody}");

            Console.WriteLine("GETリクエスト成功！");
        }
        catch (HttpRequestException e)
        {
            Console.Error.WriteLine($"HTTPリクエストエラーが発生しました: {e.Message}");
            // レスポンスがない場合の詳細なエラーハンドリング
            if (e.StatusCode.HasValue)
            {
                 Console.Error.WriteLine($"ステータスコード: {(int)e.StatusCode.Value}");
            }
        }
        catch (TaskCanceledException e)
        {
            // タイムアウトまたはCancellationTokenによるキャンセル
            Console.Error.WriteLine($"リクエストがキャンセルされました (タイムアウトなど): {e.Message}");
        }
        catch (Exception e)
        {
            Console.Error.WriteLine($"予期せぬエラーが発生しました: {e.Message}");
        }
    }
}
```

**解説:**

*   **`private static readonly HttpClient _httpClient = new HttpClient();`**: `HttpClient` のインスタンスを生成します。`HttpClient` は `IDisposable` を実装していますが、毎回 `new` するのは推奨されません（ソケット枯渇の問題が発生する可能性があります）。適切な管理方法については後述します。
*   **`_httpClient.Timeout = TimeSpan.FromSeconds(20);`**: リクエスト全体のタイムアウトを設定します。接続からレスポンスボディの読み込み完了までにかかる最大時間です。これは`HttpClient`インスタンス全体の設定です。
*   **`_httpClient.DefaultRequestHeaders.Add("Accept", "application/json");`**: 全てのリクエストにデフォルトで `Accept` ヘッダーを追加します。個別のリクエストにヘッダーを追加したい場合は `HttpRequestMessage` を使用します。
*   **`await _httpClient.GetAsync(url)`**: 非同期でGETリクエストを送信します。`await` キーワードにより、レスポンスが返ってくるまで処理が一時停止されます（ただし、スレッドはブロックされません）。
*   **`response.EnsureSuccessStatusCode()`**: レスポンスのHTTPステータスコードが2xxの範囲内であるかを確認します。2xx以外の場合、`HttpRequestException` をスローします。これにより、成功ケースとエラーケースのハンドリングを分離できます。
*   **`await response.Content.ReadAsStringAsync()`**: レスポンスボディを非同期で文字列として読み込みます。
*   **エラーハンドリング**: `HttpRequestException` はネットワークエラー、タイムアウト、`EnsureSuccessStatusCode` によるエラーなどで発生します。`TaskCanceledException` はタイムアウトまたは明示的なキャンセル時に発生します。

#### 3.2.2. POSTリクエスト (JSONボディ)

JSONデータをサーバーに送信するPOSTリクエストの例です。`.NET 5+` の `JsonContent` を使用します。

```csharp
using System;
using System.Net.Http;
using System.Net.Http.Json; // .NET 5+ で利用可能
using System.Text.Json;
using System.Threading.Tasks;

public class CSharpHttpClientPostExample
{
    private static readonly HttpClient _httpClient = new HttpClient();

    public static async Task Main(string[] args)
    {
        string url = "https://jsonplaceholder.typicode.com/posts"; // テスト用の公開API

        // 送信するJSONデータの準備（匿名型またはクラスインスタンス）
        var postData = new
        {
            title = "C# HttpClient foo",
            body = "C# HttpClient bar",
            userId = 1
        };

        try
        {
            _httpClient.Timeout = TimeSpan.FromSeconds(20);

            // POSTリクエストを非同期で送信 (JsonContentを使用)
            // JsonContentは、オブジェクトを自動的にJSONにシリアライズし、Content-Typeヘッダーを設定してくれます。
            HttpResponseMessage response = await _httpClient.PostAsJsonAsync(url, postData);

            Console.WriteLine($"Status Code: {(int)response.StatusCode} {response.StatusCode}");

            response.EnsureSuccessStatusCode(); 

            string responseBody = await response.Content.ReadAsStringAsync();
            Console.WriteLine($"Response Body:\n{responseBody}");

            Console.WriteLine("POSTリクエスト成功！");

            // レスポンスボディをJavaオブジェクトにデシリアライズする例
            // System.Text.Json は非同期デシリアライズも可能
            var responseData = JsonSerializer.Deserialize<PostResponse>(responseBody, 
                new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
            Console.WriteLine($"Parsed Response (Id): {responseData?.Id}, Title: {responseData?.Title}");
        }
        catch (HttpRequestException e)
        {
            Console.Error.WriteLine($"HTTPリクエストエラーが発生しました: {e.Message}");
            if (e.StatusCode.HasValue)
            {
                 Console.Error.WriteLine($"ステータスコード: {(int)e.StatusCode.Value}");
            }
        }
        catch (TaskCanceledException e)
        {
            Console.Error.WriteLine($"リクエストがキャンセルされました (タイムアウトなど): {e.Message}");
        }
        catch (JsonException e)
        {
            Console.Error.WriteLine($"JSON処理エラーが発生しました: {e.Message}");
        }
        catch (Exception e)
        {
            Console.Error.WriteLine($"予期せぬエラーが発生しました: {e.Message}");
        }
    }

    // レスポンスボディの構造に対応するクラス
    public class PostResponse
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string Body { get; set; }
        public int UserId { get; set; }
    }
}
```

**解説:**

*   **`using System.Net.Http.Json;`**: `.NET 5` から導入された拡張メソッド `PostAsJsonAsync` を利用するために必要です。
*   **`await _httpClient.PostAsJsonAsync(url, postData)`**: `JsonContent` を内部的に使用し、オブジェクトを自動的にJSONにシリアライズして `Content-Type: application/json` ヘッダーと共に送信します。非常に便利です。
*   **`JsonSerializer.Deserialize<PostResponse>(responseBody, ...)`**: `System.Text.Json` を使ってJSON文字列をC#オブジェクトにデシリアライズします。`PropertyNameCaseInsensitive = true` は、JSONのキー名が大文字小文字を区別しない場合に便利です（例: `userId` と `UserId`）。
*   **`StringContent` を使用したレガシーなPOST**:
    `.NET 5` より前のバージョンや、より低レベルな制御が必要な場合は、`StringContent` を直接使用できます。

    ```csharp
    // ... (前略)
    string jsonContent = JsonSerializer.Serialize(postData);
    using var content = new StringContent(jsonContent, System.Text.Encoding.UTF8, "application/json");
    HttpResponseMessage response = await _httpClient.PostAsync(url, content);
    // ... (後略)
    ```

#### 3.2.3. キャンセル可能な操作 (`CancellationToken`)

長時間実行されるリクエストや、ユーザー操作によって中断される可能性があるリクエストには、`CancellationToken` を利用することで、リクエスト処理を途中でキャンセルできます。これにより、不要なリソース消費を防ぎ、ユーザー体験を向上させます。

```csharp
using System;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;

public class CSharpHttpClientCancelExample
{
    private static readonly HttpClient _httpClient = new HttpClient();

    public static async Task Main(string[] args)
    {
        string url = "https://jsonplaceholder.typicode.com/posts/1"; 
        
        // CancellationTokenSource を作成し、キャンセルトークンを取得
        using var cts = new CancellationTokenSource();
        CancellationToken cancellationToken = cts.Token;

        try
        {
            Console.WriteLine("リクエストを送信中... (5秒後にキャンセルを試行)");

            // 別のスレッドで5秒後にキャンセルを要求
            _ = Task.Run(async () => {
                await Task.Delay(5000);
                if (!cancellationToken.IsCancellationRequested)
                {
                    cts.Cancel();
                    Console.WriteLine("--- キャンセルが要求されました ---");
                }
            });

            // リクエストにキャンセルトークンを渡す
            HttpResponseMessage response = await _httpClient.GetAsync(url, cancellationToken);

            // ここに到達した場合、キャンセルされずにレスポンスが返ってきた
            Console.WriteLine($"Status Code: {(int)response.StatusCode} {response.StatusCode}");
            response.EnsureSuccessStatusCode(); 
            string responseBody = await response.Content.ReadAsStringAsync();
            Console.WriteLine($"Response Body:\n{responseBody.Substring(0, Math.Min(responseBody.Length, 100))}...");

            Console.WriteLine("GETリクエスト成功！");
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("リクエストが正常にキャンセルされました。");
        }
        catch (HttpRequestException e)
        {
            Console.Error.WriteLine($"HTTPリクエストエラーが発生しました: {e.Message}");
        }
        catch (Exception e)
        {
            Console.Error.WriteLine($"予期せぬエラーが発生しました: {e.Message}");
        }
    }
}
```

**解説:**

*   **`CancellationTokenSource`**: キャンセル要求を生成するためのオブジェクトです。
*   **`cts.Token`**: `CancellationToken` を取得し、これを `HttpClient` のメソッドに渡します。
*   **`cts.Cancel()`**: キャンセル要求を発行します。これにより、リクエスト処理中のどこかで `OperationCanceledException` がスローされ、処理が中断されます。
*   **`OperationCanceledException`**: キャンセルによってスローされる例外です。これを適切にキャッチして処理します。

#### 3.2.4. プロフェッショナルな視点 (C#)

1.  **`HttpClient` インスタンスの適切な管理 (`IHttpClientFactory` を強く推奨)**:
    `HttpClient` は `IDisposable` を実装していますが、単純に `using` ブロックで囲んで毎回インスタンスを生成・破棄すると、**ソケット枯渇（Socket Exhaustion）** の問題を引き起こす可能性があります。これは、TCPコネクションがTIME_WAIT状態に長時間留まることで、利用可能なポートが不足する現象です。
    *   **`IHttpClientFactory` (推奨)**: .NET Core 2.1 以降で導入されたベストプラクティスです。DI (Dependency Injection) コンテナと連携し、`HttpClient` インスタンスのライフサイクルを適切に管理します。
        *   内部的に `HttpMessageHandler` をプールし、ソケット枯渇を回避します。
        *   名前付きクライアントや型付きクライアントをサポートし、異なる設定を持つ `HttpClient` を簡単に管理できます。
        *   リトライ、サーキットブレーカーなどのポリシー適用を容易にします。
    *   **シングルトンパターン (DI非利用環境での次善策)**: `IHttpClientFactory` を利用できない環境では、アプリケーション全体で単一の `HttpClient` インスタンスを使い回すのが次善策です。この場合、`HttpClient` の `Dispose()` はアプリケーション終了時に一度だけ呼び出すべきです。

    **`IHttpClientFactory` を使用した例 (ASP.NET Core の `Startup.cs` または `Program.cs`):**

    ```csharp
    // Program.cs (ASP.NET Core 6.0+ の場合)
    using Microsoft.Extensions.DependencyInjection;
    using Microsoft.Extensions.Hosting;
    using System;
    using System.Net.Http;
    using System.Threading.Tasks;

    // 型付きクライアントの定義
    public class MyApiClient
    {
        private readonly HttpClient _httpClient;

        public MyApiClient(HttpClient httpClient)
        {
            _httpClient = httpClient;
            _httpClient.BaseAddress = new Uri("https://jsonplaceholder.typicode.com/");
            _httpClient.Timeout = TimeSpan.FromSeconds(30); // クライアント固有のタイムアウト
            _httpClient.DefaultRequestHeaders.Add("Accept", "application/json");
        }

        public async Task<string> GetPostAsync(int id)
        {
            var response = await _httpClient.GetAsync($"posts/{id}");
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }

        public async Task<string> CreatePostAsync(object data)
        {
            var response = await _httpClient.PostAsJsonAsync("posts", data);
            response.EnsureSuccessStatusCode();
            return await response.Content.ReadAsStringAsync();
        }
    }

    public class Program
    {
        public static async Task Main(string[] args)
        {
            var builder = Host.CreateDefaultBuilder(args);
            builder.ConfigureServices((hostContext, services) =>
            {
                // IHttpClientFactory を利用して MyApiClient を登録
                services.AddHttpClient<MyApiClient>();

                // 他のサービスが必要な場合はここで登録
                // services.AddTransient<SomeOtherService>();
            });

            var host = builder.Build();

            // Host経由で MyApiClient を取得し使用
            using (var scope = host.Services.CreateScope())
            {
                var myApiClient = scope.ServiceProvider.GetRequiredService<MyApiClient>();
                
                Console.WriteLine("--- Fetching post 1 ---");
                string post1 = await myApiClient.GetPostAsync(1);
                Console.WriteLine(post1.Substring(0, Math.Min(post1.Length, 100)) + "...");

                Console.WriteLine("\n--- Creating new post ---");
                var newPost = new { title = "My New Post", body = "Hello HttpClientFactory!", userId = 99 };
                string createdPost = await myApiClient.CreatePostAsync(newPost);
                Console.WriteLine(createdPost.Substring(0, Math.Min(createdPost.Length, 100)) + "...");
            }
            // await host.RunAsync(); // 通常はWebアプリケーションとして実行
        }
    }
    ```

2.  **メモリ効率と大きなレスポンスボディ**:
    Javaと同様に、非常に大きなレスポンスボディを扱う場合、`ReadAsStringAsync()` で全てをメモリにロードするのは危険です。
    *   `await response.Content.ReadAsStreamAsync()`: レスポンスボディを `Stream` として扱い、ストリーミング処理を行うことができます。
3.  **適切なタイムアウト設定**:
    `HttpClient.Timeout` プロパティでリクエスト全体のタイムアウトを設定します。これは `HttpRequestException` または `TaskCanceledException` を引き起こします。
    `IHttpClientFactory` を利用する場合は、クライアントごとにタイムアウトを設定できます。
4.  **JSONシリアライゼーション/デシリアライゼーション**:
    `System.Text.Json` が現在推奨されるJSONライブラリです。高パフォーマンスであり、.NET Core/5+ で標準提供されます。
    *   `JsonSerializerOptions` を利用して、プロパティ名の大文字小文字を区別しない設定や、日付のフォーマット、NULL値の扱いなどをカスタマイズできます。
5.  **例外処理のベストプラクティス**:
    *   `HttpRequestException`: ネットワークの問題、DNS解決失敗、接続拒否、`EnsureSuccessStatusCode()` によって発生するHTTPエラーなど。
    *   `TaskCanceledException` / `OperationCanceledException`: タイムアウトまたは明示的なキャンセルによって発生。
    *   これらの例外は、適切にキャッチし、ログに記録し、リトライなどの回復戦略を検討します。
6.  **ロギング**:
    `Microsoft.Extensions.Logging` を利用し、DIを通じてロガーを注入してログを出力します。HTTPリクエスト/レスポンスの詳細なロギングは、開発・デバッグ時には有用ですが、本番環境ではパフォーマンスとセキュリティを考慮し、ログレベルを適切に設定してください。
7.  **テスト容易性**:
    `IHttpClientFactory` を使用することで、`HttpClient` のモック化が非常に容易になります。`HttpMessageHandler` をモック化することで、外部APIへの実際のリクエストなしにクライアントロジックをテストできます。
    *   `HttpClientFactory.CreateClient()` は `HttpMessageHandler` を内部で利用しており、これをモックに差し替えることで、外部呼び出しをシミュレートできます。

---

## 4. 共通の考慮事項とベストプラクティス

JavaとC#の両方に共通する、堅牢なHTTP/REST APIクライアントを構築するための重要な考慮事項です。

### 4.1. リトライ戦略

一時的なネットワーク障害、レートリミット、サービスの一時的な過負荷などにより、APIリクエストが失敗することがあります。このような場合に、何度かリクエストを再試行するリトライ戦略はアプリケーションの堅牢性を高めます。

*   **冪等なリクエストに限定**: GETリクエストのように、何度実行しても結果が変わらない（副作用がない）リクエストにのみ適用するのが安全です。POSTやPUTなど副作用のあるリクエストは、サーバー側が冪等性を保証している場合を除き、慎重に適用してください。
*   **指数バックオフ**: リトライ間隔を徐々に長くしていくことで、サーバーへの負荷を軽減し、回復の機会を与えます。（例: 1秒後、2秒後、4秒後、...）
*   **最大リトライ回数**: 無限にリトライしないよう、最大リトライ回数を設定します。
*   **ジッター**: リトライ間隔にランダムな要素（ジッター）を加えることで、多数のクライアントが一斉にリトライを開始し、サーバーに更なる負荷をかける「サンダーストーム問題」を回避します。
*   **ライブラリの利用**:
    *   Java: [Resilience4j](https://resilience4j.github.io/resilience4j/)
    *   C#: [Polly](https://github.com/App-vNext/Polly)

### 4.2. サーキットブレーカーパターン

外部サービスが完全にダウンしている場合や、応答が非常に遅い場合に、失敗するリクエストを繰り返し送り続けると、自サービスのリソース（スレッド、CPUなど）を枯渇させてしまう可能性があります。サーキットブレーカーパターンは、このような状況を防ぐためのメカニズムです。

*   **状態**: 「閉（Closed）」「開（Open）」「半開（Half-Open）」の3つの状態を持ちます。
    *   **閉**: 通常通りリクエストを許可します。エラーが増えると「開」に移行。
    *   **開**: リクエストをブロックし、即座にエラーを返します（外部サービスへの呼び出しを行いません）。一定時間経過すると「半開」に移行。
    *   **半開**: 少数のリクエストのみを外部サービスに送り、成功すれば「閉」に、失敗すれば再度「開」に移行。
*   **メリット**: 外部サービスの障害が自サービスに波及するのを防ぎ、迅速なフェイルファストを実現し、外部サービスの回復を待つ間にリソースを保護します。
*   **ライブラリの利用**:
    *   Java: [Resilience4j](https://resilience4j.github.io/resilience4j/)
    *   C#: [Polly](https://github.com/App-vNext/Polly)

### 4.3. ロギング

HTTP通信は、問題発生時の調査に不可欠な情報源となります。

*   **詳細レベル**: 開発・デバッグ環境ではリクエスト/レスポンスのヘッダーやボディを含めた詳細なロギングが役立ちます。本番環境では、パフォーマンスへの影響と機密情報の漏洩リスクを考慮し、エラーや警告レベルのログに限定したり、ボディをマスクしたりすることが一般的です。
*   **相関ID (Correlation ID)**: リクエストの最初から最後まで追跡できるように、一意のIDを生成し、HTTPヘッダーとしてAPIリクエストに含めるようにします。サーバー側でもこのIDをログに出力することで、分散システム全体でのリクエストフローを追跡できます。

### 4.4. セキュリティ

外部APIと通信する際には、セキュリティ上の考慮が必要です。

*   **HTTPSの強制**: 全てのAPI通信はHTTPS（TLS/SSL）を使用し、盗聴や改ざんから保護する必要があります。
*   **認証・認可情報の安全な管理**:
    *   **APIキー**: 環境変数、シークレットマネージャー、設定ファイルなどで管理し、コードに直接ハードコードしないでください。
    *   **OAuth2/JWT**: アクセストークンをHTTPヘッダー（`Authorization: Bearer <token>`）で送信するのが一般的です。トークンの有効期限管理やリフレッシュメカニズムも考慮します。
*   **SSL証明書の検証**: 自己署名証明書や信頼できない証明書を使用しているAPIには、セキュリティリスクがあるため注意が必要です。本番環境では常に有効な証明書を検証するように設定してください。

### 4.5. テスト容易性

実装されたHTTPクライアントの単体テストや統合テストを容易にする設計が重要です。

*   **インターフェースベースの設計**: HTTPクライアントの具体的な実装を直接使用するのではなく、インターフェースを介して依存性注入（DI）することで、テスト時にモックやスタブに置き換えやすくなります。
*   **モックサーバーの利用**: [WireMock](http://wiremock.org/) (Java), [Mockoon](https://mockoon.com/) (汎用) などのツールを使用して、テスト中にダミーのAPIサーバーを立て、実際の外部APIへの呼び出しなしにクライアントの動作を検証できます。

---

## まとめ

このリファレンスでは、JavaとC#におけるHTTP通信・REST APIクライアントの実装について、基本的なコード例からプロフェッショナルな視点での考慮事項までを解説しました。

**重要なポイントの再確認:**

*   **Java**: `java.net.http.HttpClient` (Java 11+) を推奨。`HttpClient` と `ObjectMapper` はシングルトンとして使い回す。
*   **C#**: `System.Net.Http.HttpClient` を推奨。`IHttpClientFactory` を利用して管理する。
*   **非同期処理**: Javaでは `CompletableFuture`、C#では `async`/`await` を活用し、UIスレッドやメインスレッドをブロックしない。
*   **エラーハンドリング**: ネットワークエラー、タイムアウト、HTTPステータスコードによるエラーを適切に処理する。
*   **堅牢性**: リトライ戦略、サーキットブレーカーパターンを適用し、外部サービスの障害から自サービスを保護する。
*   **セキュリティ**: HTTPS、認証情報の安全な管理を徹底する。
*   **テスト容易性**: インターフェースベースの設計とモック化を考慮する。

これらのガイドラインとコード例が、皆さんの日々の開発作業の一助となり、チーム全体の技術力向上に繋がることを期待しています。不明な点があれば、いつでもチーム内で相談してください。常に最新の情報をキャッチアップし、より良いコードを目指していきましょう！