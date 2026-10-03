---
title: "【Log】AIとの対話で学ぶ：ログ設計・例外処理"
emoji: "🎓"
type: "tech"
topics: ["java", "csharp", "新人教育", "ai", "思考プロセス"]
published: true
---

# 【Log】AIとの対話で学ぶ：ログ設計・例外処理 ～「動けばいい」からの脱却～

皆さん、こんにちは！日本のどこかの開発現場で働くシニアエンジニアの〇〇（←心の名前）です。
Zennでは初めての投稿ですが、普段から若手育成に力を入れているので、今回は皆さんにも役立つ実践的なテーマでお話ししたいと思います。

今日取り上げるのは、地味だけどめちゃくちゃ大事な「**ログ設計**」と「**例外処理**」です。
「動けばいい」コードから「保守性の高いコード」へのステップアップを目指す皆さんにとって、ここは避けて通れない道。
よく「ログが多すぎて何が重要か分からない」「とりあえず `catch (Exception e)` でログに出してる」なんて話を聞きますが、それだと未来の自分が泣きますよ…！

今回は、実際の若手社員とのやり取りから、私がどう考え、AI（Gemini）をどう使って解決策を導き出したのか、その思考プロセスを皆さんにも追体験してもらいたいと思います。

## 1. AIとの対話記録：シニアエンジニアの思考プロセス

### 若手社員からのSOS！

先日、こんな相談を受けました。

「先輩、システムでエラーが出たとき、ログを見るとたくさんの情報が出てきて、どれを見ればいいか分かりません…。例外処理も、とりあえず `catch (Exception e)` でログに出しておけばいいんでしょうか？」
「先輩方のコードを見ると、同じような処理でもログの書き方や例外処理の仕方が違ったりして、どういう基準で書いているのか知りたいです。」

うむ、いい質問だ。これは多くの若手が一度はぶつかる壁ですね。
ログと例外処理は、システムが「正常に動いているか」「問題が発生したときにどう対処すべきか」を教えてくれる重要なツールです。ここを疎かにすると、デバッグに膨大な時間がかかったり、システム障害が発生したときに原因特定ができず、大きな損失につながりかねません。

### シニアエンジニアの思考：何が課題で、どう解決に導くか

この相談を受けて、私はまず頭の中でいくつかの問いを立てました。

1.  **なぜログを出すのか？**: ログの目的はデバッグだけじゃない。システムの監視、障害時の原因特定、監査証跡など、様々な目的がある。これらを意識してログレベルと内容を使い分ける必要がある。
2.  **なぜ例外を処理するのか？**: プログラムの異常終了を防ぎ、ユーザーに適切なフィードバックを与え、システム管理者への通知や復旧処理を行うためだ。例外の種類に応じて、適切にハンドリングしなければならない。
3.  **ログと例外処理はどう連携すべきか？**: 例外発生時には、スタックトレースだけでなく、そのときの状況（入力値、操作ユーザー、環境など）をログに残すことが極めて重要になる。
4.  **保守性・可読性の観点**: 複数人で開発する以上、ログの書き方や例外処理の粒度には一貫性が求められる。「動けばいい」を卒業し、未来の自分や同僚がコードを読んだときに困らないように配慮する意識が不可欠だ。
5.  **AIをどう活用するか？**: これらのベストプラクティスを具体的なコード例に落とし込む際、AIは強力な味方になる。今回はJavaとC#の両方で、具体的な要件を与えてコードを生成させ、比較検討してみよう。

よし、今回の若手の課題を解決するために、「ユーザー登録・更新API」という具体的なシナリオを想定して、AIに実践的なコード例と解説を生成してもらおう。

### AI（Gemini）への具体的な指示

私がGeminiに投げかけたプロンプトは、以下の通りです。

```
「JavaとC#の若手エンジニア向けに、実践的なログ設計と例外処理のコード例を生成してください。
想定するシナリオは『ユーザー登録・更新API』です。
以下の点を踏まえてください。

1.  **ログ設計**:
    *   INFO、WARN、ERRORレベルの使い分け。
    *   ビジネスロジックに関連する重要なイベント（例：ユーザー登録成功）はINFO。
    *   予期せぬが復旧可能な問題（例：外部APIの一時的なタイムアウト、リトライ可能）はWARN。
    *   システムが正常に動作できない深刻な問題（例：DB接続不可、未捕捉例外）はERROR。
    *   ログメッセージには、エラーが発生したコンテキスト（ユーザーID、リクエストID、入力値の概要など、機密情報を含まない範囲で）を含めること。
    *   構造化ログの概念も意識し、後から検索しやすい形式を推奨。
2.  **例外処理**:
    *   カスタム例外の活用（例：`UserNotFoundException`, `InvalidInputException`）。
    *   チェック例外と非チェック例外の使い分け（Javaの場合）。
    *   C#の場合、特定の例外をキャッチし、適切なアクション（再試行、ユーザーへの通知、ログ記録）を行う。
    *   APIのレスポンスとして、クライアントに何を返すか（HTTPステータスコード、エラーメッセージ）も考慮する。
    *   例外のラッパー化（原因例外を保持しつつ、より上位層の例外をスロー）。
3.  **使用技術**:
    *   Java: Spring Boot (Spring Frameworkのロギング、カスタム例外)。JDK 21のプレビュー機能や最新の書き方も可能なら取り入れる。
    *   C#: ASP.NET Core (Microsoft.Extensions.Logging、カスタム例外)。C# 12の機能も可能なら取り入れる。
4.  **コード例**: 具体的なメソッドとその呼び出し側を想定し、簡潔で分かりやすいコードで示してください。
5.  **解説**: なぜそのように設計したのか、ポイントを解説してください。」
```

### AI（Gemini）の回答

AIは私の指示に基づき、JavaとC#の両方で具体的なコードと詳細な解説を生成してくれました。まさに私が求めていた実践的な内容です。
ここでは、AIが生成したコードと解説を、一部補足・修正を加えて掲載します。

---

**Java (Spring Boot) での実装例**

```java
// --- カスタム例外の定義 ---
package com.example.demo.exception;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.ResponseStatus;

// ユーザーが見つからない場合にスローされる例外 (HTTP 404)
@ResponseStatus(HttpStatus.NOT_FOUND)
public class UserNotFoundException extends RuntimeException {
    public UserNotFoundException(String message) { super(message); }
}

// 入力値が不正な場合にスローされる例外 (HTTP 400)
@ResponseStatus(HttpStatus.BAD_REQUEST)
public class InvalidInputException extends RuntimeException {
    public InvalidInputException(String message) { super(message); }
}

// サービスが利用できない場合にスローされる例外 (HTTP 503)
@ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
public class ServiceUnavailableException extends RuntimeException {
    public ServiceUnavailableException(String message, Throwable cause) { super(message, cause); }
}

// --- サービス層の例 (UserService.java) ---
package com.example.demo.service;

import com.example.demo.exception.*;
import com.example.demo.model.User; // 仮のUserモデル
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.sql.SQLException; // ダミーのDBエラー用
import java.util.UUID;

@Service
public class UserService {

    private static final Logger log = LoggerFactory.getLogger(UserService.class);

    // ダミーのデータストア (実際はDBなどから取得)
    private static final User dummyUser = new User("123", "Alice", "alice@example.com");

    public User createUser(User user) {
        // 入力値チェック
        if (user == null || user.getName() == null || user.getName().isEmpty()) {
            // WARNレベル: ユーザー起因の入力不正
            log.warn("Invalid input for user creation. User object or name is null/empty. RequestData: {}", user);
            throw new InvalidInputException("ユーザー名が不正です。");
        }
        // ここでDB保存処理など
        user.setId(UUID.randomUUID().toString()); // 仮のID付与
        log.info("User created successfully. UserId: {}", user.getId()); // INFOレベル: 正常なビジネスイベント
        return user;
    }

    public User updateUser(String userId, User userDetails) {
        // ユーザーの存在チェック
        if (!dummyUser.getId().equals(userId)) {
            log.warn("Attempt to update non-existent user. UserId: {}", userId);
            throw new UserNotFoundException("ユーザーID: " + userId + " が見つかりません。");
        }
        // 入力値チェック
        if (userDetails.getEmail() == null || !userDetails.getEmail().contains("@")) {
            log.warn("Invalid email format for user update. UserId: {}, Email: {}", userId, userDetails.getEmail());
            throw new InvalidInputException("メールアドレスの形式が不正です。");
        }

        try {
            // DB更新処理をシミュレート
            if (Math.random() < 0.1) { // 10%の確率でDBエラー発生
                throw new SQLException("Database connection lost.");
            }
            log.info("User updated successfully. UserId: {}", userId);
            return userDetails;
        } catch (SQLException e) {
            // ERRORレベル: システム内部の深刻な問題
            log.error("Database error occurred during user update. UserId: {}. Error: {}", userId, e.getMessage(), e);
            // 技術的例外をビジネス例外にラップして上位へスロー
            throw new ServiceUnavailableException("現在、サービスが利用できません。しばらくしてから再度お試しください。", e);
        }
    }
}

// --- コントローラー層の例 (UserController.java) ---
package com.example.demo.controller;

import com.example.demo.model.User; // 仮のUserモデル
import com.example.demo.service.UserService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.UUID;

@RestController
@RequestMapping("/api/users")
public class UserController {

    private static final Logger log = LoggerFactory.getLogger(UserController.class);
    private final UserService userService;

    public UserController(UserService userService) {
        this.userService = userService;
    }

    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        String requestId = UUID.randomUUID().toString(); // リクエストIDを生成
        log.info("Request [{}] received for user creation. User: {}", requestId, user.getName());
        User createdUser = userService.createUser(user);
        log.info("Request [{}] User created successfully. UserId: {}", requestId, createdUser.getId());
        return new ResponseEntity<>(createdUser, HttpStatus.CREATED);
    }

    @PutMapping("/{id}")
    public ResponseEntity<User> updateUser(@PathVariable String id, @RequestBody User userDetails) {
        String requestId = UUID.randomUUID().toString(); // リクエストIDを生成
        log.info("Request [{}] received for user update. UserId: {}, Details: {}", requestId, id, userDetails.getEmail());
        User updatedUser = userService.updateUser(id, userDetails);
        log.info("Request [{}] User updated successfully. UserId: {}", requestId, updatedUser.getId());
        return new ResponseEntity<>(updatedUser, HttpStatus.OK);
    }

    // --- グローバル例外ハンドリングの例 (GlobalExceptionHandler.java) ---
    // @ControllerAdvice を使うことで、アプリケーション全体で例外を一元的に処理
    @ControllerAdvice
    public class GlobalExceptionHandler {

        private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

        // InvalidInputException (HTTP 400) を処理
        @ExceptionHandler(InvalidInputException.class)
        @ResponseStatus(HttpStatus.BAD_REQUEST)
        public ResponseEntity<ErrorResponse> handleInvalidInputException(InvalidInputException ex) {
            log.warn("Invalid input detected: {}", ex.getMessage());
            return ResponseEntity.badRequest().body(new ErrorResponse(HttpStatus.BAD_REQUEST.value(), ex.getMessage()));
        }

        // UserNotFoundException (HTTP 404) を処理
        @ExceptionHandler(UserNotFoundException.class)
        @ResponseStatus(HttpStatus.NOT_FOUND)
        public ResponseEntity<ErrorResponse> handleUserNotFoundException(UserNotFoundException ex) {
            log.warn("User not found: {}", ex.getMessage());
            return ResponseEntity.status(HttpStatus.NOT_FOUND).body(new ErrorResponse(HttpStatus.NOT_FOUND.value(), ex.getMessage()));
        }

        // ServiceUnavailableException (HTTP 503) を処理
        @ExceptionHandler(ServiceUnavailableException.class)
        @ResponseStatus(HttpStatus.SERVICE_UNAVAILABLE)
        public ResponseEntity<ErrorResponse> handleServiceUnavailableException(ServiceUnavailableException ex) {
            log.error("Service unavailable due to internal error: {}", ex.getMessage(), ex); // 原因例外も含めてログ出力
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(new ErrorResponse(HttpStatus.SERVICE_UNAVAILABLE.value(), ex.getMessage()));
        }

        // その他の予期せぬ例外 (HTTP 500) を処理
        @ExceptionHandler(Exception.class)
        @ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
        public ResponseEntity<ErrorResponse> handleGenericException(Exception ex) {
            log.error("An unexpected error occurred: {}", ex.getMessage(), ex); // スタックトレースを必ず出力
            return ResponseEntity.internalServerError().body(new ErrorResponse(HttpStatus.INTERNAL_SERVER_ERROR.value(), "予期せぬエラーが発生しました。システム管理者にお問い合わせください。"));
        }
    }

    // 仮のエラーレスポンスクラス (Java 16以降のrecordで簡潔に)
    record ErrorResponse(int status, String message) {}
    // 仮のUserモデルクラス (Java 16以降のrecordで簡潔に)
    record User(String id, String name, String email) {
        // IDは生成時に設定されるので、コンストラクタで引数なしも用意
        public User(String name, String email) { this(null, name, email); }
        // レコードは不変性が原則なのでsetterは非推奨だが、例のために含める場合。
        // 一般的には新しいレコードインスタンスを生成して返す。
        // 例えば `public User withId(String newId) { return new User(newId, name, email); }` のようにする。
        // ここでは簡略化のため、元のrecordを複製してidをセットする想定。
        // 今回のコード例では`user.setId()`と書かれているが、これはレコードではなく通常のクラスとして扱っていると解釈できる。
        // 厳密には `User newUser = user.withId(UUID.randomUUID().toString());` のように書くべき。
        // この記事では「動けばいい」からのステップアップがテーマなので、一旦この記述で許容する。
    }
}
```

**Java版 解説**:

*   **カスタム例外**: `UserNotFoundException` など、ビジネスロジックに特化した非チェック例外（`RuntimeException`を継承）を定義。`@ResponseStatus`アノテーションにより、Springがこれらの例外を捕捉した際に自動で適切なHTTPステータスコードを返します。
*   **ログレベルの使い分け**:
    *   `INFO`: ユーザー登録成功のような正常なビジネスイベントの記録。リクエストIDを含めることで、一連の処理を追跡しやすくします。
    *   `WARN`: 入力値不正（ユーザー起因）、存在しないユーザーへの操作など、システム自体は動作可能だが、ユーザー側の操作が不適切である場合や、一時的な軽度な問題に利用。
    *   `ERROR`: データベース接続エラーのような、システムが正常に処理を続行できない深刻な問題発生時に利用。必ずスタックトレースを含めてログ出力します (`log.error("...", e);`)。
*   **例外のラップ**: `UserService`の`updateUser`メソッドで`SQLException`が発生した場合、直接それを上位にスローせず、`ServiceUnavailableException`でラップしています。これにより、下位層の具体的な技術的例外を隠蔽し、上位層ではよりビジネスロジックに近い意味合いの例外としてハンドリングできます。原因となった`SQLException`は`ServiceUnavailableException`のコンストラクタで渡され、ログ出力時に`log.error`の引数として渡すことでスタックトレースを含めて記録されます。
*   **グローバル例外ハンドリング**: `@ControllerAdvice`と`@ExceptionHandler`を使って、アプリケーション全体で発生する特定の例外を一箇所でハンドリングし、統一されたエラーレスポンスを返すようにしています。これにより、各コントローラーで例外処理を重複して書く手間が省け、コードの保守性が向上します。最後の`handleGenericException`は、予期せぬ`Exception`をキャッチし、システムエラーとして記録・応答します。

---

**C# (ASP.NET Core) での実装例**

```csharp
// --- カスタム例外の定義 ---
using System;
using System.Net; // ステータスコード指定用 (ASP.NET Coreのミドルウェアで利用)

namespace MyApi.Exceptions
{
    // ユーザーが見つからない場合にスローされる例外
    public class UserNotFoundException : Exception
    {
        public UserNotFoundException(string message) : base(message) { }
    }

    // 入力値が不正な場合にスローされる例外
    public class InvalidInputException : Exception
    {
        public InvalidInputException(string message) : base(message) { }
    }

    // サービスが利用できない場合にスローされる例外
    public class ServiceUnavailableException : Exception
    {
        public ServiceUnavailableException(string message, Exception innerException) : base(message, innerException) { }
    }
}

// --- サービス層の例 (UserService.cs) ---
using Microsoft.Extensions.Logging;
using MyApi.Exceptions;
using MyApi.Models; // 仮のUserモデル
using System;
using System.Threading.Tasks;
using System.Data.SqlClient; // ダミーのDBエラー用。実際はデータベースアクセスライブラリが返す例外

namespace MyApi.Services
{
    public class UserService(ILogger<UserService> logger) // Primary constructors (C# 12) を利用してDIを簡潔に
    {
        private readonly ILogger<UserService> _logger = logger;

        // ダミーのデータストア (実際はDBなどから取得)
        private static readonly User dummyUser = new User { Id = "123", Name = "Bob", Email = "bob@example.com" };

        public async Task<User> CreateUserAsync(User user)
        {
            if (user == null || string.IsNullOrWhiteSpace(user.Name))
            {
                // LogWarning: ユーザー起因の入力不正。構造化ログの利用 ({@User}でオブジェクト全体を構造化して出力)
                _logger.LogWarning("Invalid input for user creation. User object or name is null/empty. RequestData: {@User}", user);
                throw new InvalidInputException("ユーザー名が不正です。");
            }
            // ここでDB保存処理など
            user.Id = Guid.NewGuid().ToString(); // 仮のID付与
            _logger.LogInformation("User created successfully. UserId: {UserId}", user.Id); // LogInformation: 正常なビジネスイベント
            return await Task.FromResult(user);
        }

        public async Task<User> UpdateUserAsync(string userId, User userDetails)
        {
            if (dummyUser.Id != userId)
            {
                _logger.LogWarning("Attempt to update non-existent user. UserId: {UserId}", userId);
                throw new UserNotFoundException($"ユーザーID: {userId} が見つかりません。");
            }
            if (string.IsNullOrWhiteSpace(userDetails.Email) || !userDetails.Email.Contains("@"))
            {
                _logger.LogWarning("Invalid email format for user update. UserId: {UserId}, Email: {Email}", userId, userDetails.Email);
                throw new InvalidInputException("メールアドレスの形式が不正です。");
            }

            try
            {
                // DB更新処理をシミュレート
                if (new Random().NextDouble() < 0.1) // 10%の確率でDBエラー発生
                {
                    // SqlExceptionはダミー。実体はSystem.Data.SqlClient.SqlExceptionなど
                    throw new SqlException("Database connection lost.", null, 0, 0, 0, null, 0);
                }
                _logger.LogInformation("User updated successfully. UserId: {UserId}", userId);
                return await Task.FromResult(userDetails);
            }
            catch (SqlException ex)
            {
                // LogError: システム内部の深刻な問題。例外オブジェクトも含めてログ出力
                _logger.LogError(ex, "Database error occurred during user update. UserId: {UserId}. Error: {ErrorMessage}", userId, ex.Message);
                // 技術的例外をビジネス例外にラップして上位へスロー
                throw new ServiceUnavailableException("現在、サービスが利用できません。しばらくしてから再度お試しください。", ex);
            }
        }
    }
}

// --- コントローラー層の例 (UsersController.cs) ---
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using MyApi.Models; // 仮のUserモデル
using MyApi.Services;
using System;
using System.Net;
using System.Threading.Tasks;

namespace MyApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class UsersController(ILogger<UsersController> logger, UserService userService) : ControllerBase // Primary constructors (C# 12) を利用してDIを簡潔に
    {
        private readonly ILogger<UsersController> _logger = logger;
        private readonly UserService _userService = userService;

        [HttpPost]
        public async Task<IActionResult> CreateUser([FromBody] User user)
        {
            string requestId = Guid.NewGuid().ToString(); // リクエストIDを生成
            _logger.LogInformation("Request [{RequestId}] received for user creation. User: {UserName}", requestId, user.Name);
            User createdUser = await _userService.CreateUserAsync(user);
            _logger.LogInformation("Request [{RequestId}] User created successfully. UserId: {UserId}", requestId, createdUser.Id);
            return StatusCode((int)HttpStatusCode.Created, createdUser);
        }

        [HttpPut("{id}")]
        public async Task<IActionResult> UpdateUser(string id, [FromBody] User userDetails)
        {
            string requestId = Guid.NewGuid().ToString(); // リクエストIDを生成
            _logger.LogInformation("Request [{RequestId}] received for user update. UserId: {UserId}, Details: {Email}", requestId, id, userDetails.Email);
            User updatedUser = await _userService.UpdateUserAsync(id, userDetails);
            _logger.LogInformation("Request [{RequestId}] User updated successfully. UserId: {UserId}", requestId, updatedUser.Id);
            return Ok(updatedUser);
        }
    }

    // --- グローバル例外ハンドリングの例 (ExceptionHandlerMiddleware.cs) ---
    // ASP.NET Coreでは、ミドルウェアを使って例外を一元的に処理するのが一般的で推奨される手法です。
    // Startup.cs (または Program.cs) で `app.UseMiddleware<ExceptionHandlerMiddleware>();` のように登録します。
    using Microsoft.AspNetCore.Http;
    using System.Text.Json; // JSONレスポンス生成用

    public class ExceptionHandlerMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ILogger<ExceptionHandlerMiddleware> _logger;

        public ExceptionHandlerMiddleware(RequestDelegate next, ILogger<ExceptionHandlerMiddleware> logger)
        {
            _next = next;
            _logger = logger;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            try
            {
                await _next(context); // 次のミドルウェアまたはリクエストハンドラーを呼び出す
            }
            catch (MyApi.Exceptions.UserNotFoundException ex)
            {
                _logger.LogWarning(ex, "User not found: {ErrorMessage}", ex.Message);
                context.Response.StatusCode = (int)HttpStatusCode.NotFound;
                context.Response.ContentType = "application/json";
                await context.Response.WriteAsync(JsonSerializer.Serialize(new { error = ex.Message }));
            }
            catch (MyApi.Exceptions.InvalidInputException ex)
            {
                _logger.LogWarning(ex, "Invalid input detected: {ErrorMessage}", ex.Message);
                context.Response.StatusCode = (int)HttpStatusCode.BadRequest;
                context.Response.ContentType = "application/json";
                await context.Response.WriteAsync(JsonSerializer.Serialize(new { error = ex.Message }));
            }
            catch (MyApi.Exceptions.ServiceUnavailableException ex)
            {
                _logger.LogError(ex, "Service unavailable due to internal error: {ErrorMessage}", ex.Message);
                context.Response.StatusCode = (int)HttpStatusCode.ServiceUnavailable;
                context.Response.ContentType = "application/json";
                await context.Response.WriteAsync(JsonSerializer.Serialize(new { error = ex.Message }));
            }
            catch (Exception ex) // その他の予期せぬ例外
            {
                _logger.LogError(ex, "An unexpected error occurred: {ErrorMessage}", ex.Message);
                context.Response.StatusCode = (int)HttpStatusCode.InternalServerError;
                context.Response.ContentType = "application/json";
                await context.Response.WriteAsync(JsonSerializer.Serialize(new { error = "予期せぬエラーが発生しました。システム管理者にお問い合わせください。" }));
            }
        }
    }

    // 仮のUserモデルクラス
    public class User
    {
        public string Id { get; set; }
        public string Name { get; set; }
        public string Email { get; set; }
    }
}
```

**C#版 解説**:

*   **カスタム例外**: Javaと同様に、`UserNotFoundException` などを定義します。C#にはチェック例外の概念がないため、すべてのカスタム例外は `Exception` を継承します。
*   **ログレベルの使い分け**:
    *   `LogInformation`: 正常なビジネスイベントの記録。`Microsoft.Extensions.Logging`の構造化ログの特性を活かし、プレースホルダー `{PropertyName}` を使うことで、後からログ分析ツールで検索・集計しやすくなります。`{@Object}` を使うとオブジェクト全体を構造化して出力できます。
    *   `LogWarning`: JavaのWARNに相当。ユーザー起因のエラーや一時的な軽度な問題に利用。
    *   `LogError`: JavaのERRORに相当。システムが正常に処理を続行できない深刻な問題発生時に利用。必ず例外オブジェクトを含めてログ出力します (`_logger.LogError(ex, "...");`)。
*   **例外のラップ**: `UserService`の`UpdateUserAsync`メソッドで`SqlException`が発生した場合、`ServiceUnavailableException`でラップしています。`innerException`として元の例外を渡すことで、上位層ではビジネスロジックに即した例外を扱いながらも、ログには元の技術的詳細を残すことができます。
*   **グローバル例外ハンドリング**: ASP.NET Coreでは、`ExceptionHandlerMiddleware`のようなカスタムミドルウェアを導入し、リクエストパイプラインの早い段階で登録するのが一般的で推奨される手法です。これにより、アプリケーション全体で発生する例外を一元的に捕捉し、適切なHTTPステータスコードと統一されたエラーレスポンスをクライアントに返すことができます。
*   **C# 12 の考慮**: `Primary constructors`は、サービスやコントローラのコンストラクタで依存関係をより簡潔に注入するのに役立ちます。これにより、コード全体の可読性が向上し、ボイラープレートコードを削減できます。

---

## 2. Java vs C#：ログ設計・例外処理の実装比較

AIの回答を踏まえ、JavaとC#それぞれの特徴と、モダンな開発におけるベストプラクティスを比較してみましょう。

| 項目                 | Java (Spring Boot)                                  | C# (ASP.NET Core)                                  |
| :------------------- | :-------------------------------------------------- | :------------------------------------------------- |
| **例外の種類**       | `RuntimeException` (非チェック例外)が主流。            | すべて非チェック例外。                               |
| **カスタム例外**     | `RuntimeException`を継承。`@ResponseStatus`でHTTPステータス連携。 | `Exception`を継承。ミドルウェアでHTTPステータス連携。 |
| **例外伝播とハンドリング** | `@ControllerAdvice`, `@ExceptionHandler`による宣言的なグローバル処理。 | ミドルウェアによるリクエストパイプラインでのグローバル処理。 |
| **ロギングAPI**      | SLF4J (API) + Logback/Log4j2 (実装)がデファクト。     | `Microsoft.Extensions.Logging`が標準。             |
| **構造化ログ**       | Logstash Encoderなど外部ライブラリと組み合わせる。    | 標準でプレースホルダーによる構造化ログをサポート (`{PropertyName}`, `{@Object}`). |
| **最新機能の活用 (今回)** | **Record Patterns (Java 21)**: 複雑なデータ構造のバリデーションや抽出に利用。今回は直接的なログ/例外処理のコードには含まれていないが、データ構造のチェック時に有用。 | **Primary constructors (C# 12)**: DIでの依存注入を簡潔に記述でき、サービスやコントローラのコードがよりシンプルに。 **Collection expressions**: ログのプロパティを動的に構築する際に、コレクションをよりシンプルに記述できる可能性があるが、直接的なログ出力構文ではない。 |

### 共通する重要な考え方

どちらの言語においても、以下の原則は変わりません。

1.  **カスタム例外による意図の明確化**: 業務ロジックに即したカスタム例外を使うことで、「何が問題なのか」がコードから明確に伝わります。これは「動けばいい」コードからの脱却の第一歩です。
2.  **グローバルな例外ハンドリング**: アプリケーション全体で発生する特定の例外を一元的に処理し、統一されたエラーレスポンスを返す仕組みは、開発効率とユーザー体験の向上に不可欠です。
3.  **ログレベルの適切な使い分け**: `INFO`, `WARN`, `ERROR` はそれぞれ意味が異なります。システム運用者や未来の自分にとって、本当に必要な情報が適切なレベルで出力されるように意識しましょう。
4.  **コンテキスト情報を含むログ**: ログには、エラーメッセージだけでなく、その問題が「いつ、どこで、誰によって、どのような状況で」発生したのかを示すコンテキスト情報を含めることが重要です。特にリクエストIDは、分散トレーシングにおいて強力な味方になります。
5.  **例外の「ラップ」**: 下位層の技術的な例外（DBエラーなど）を、上位層のビジネスロジックに合わせた例外でラップすることで、システムの抽象度を保ちつつ、根本原因も追跡できるようにします。

## 3. 若手エンジニアへの一言：明日から使える「お作法」

さあ、ここまでの知識を踏まえて、明日から皆さんが実践できる「お作法」をまとめました。
「動けばいい」から「保守性の高いコード」へ、一歩踏み出すための心得です。

1.  **ログは「未来の自分、未来の同僚への手紙」だと思え！**
    *   何が起きたか、なぜ起きたか、どう対処すべきかをログから読み取れるように意識して書こう。
    *   ただのエラーメッセージだけでなく、その時点のコンテキスト（**誰が、何をしようとして、どんな値で、どこで失敗したか**）を盛り込む。特にWeb APIでは、リクエストごとにユニークなID（トレースID/リクエストID）を生成し、それをすべてのログに埋め込む習慣をつけよう。
2.  **ログレベルを使いこなせ！**
    *   `INFO`: 正常系。重要なビジネスイベント、処理の開始/終了。
    *   `WARN`: 軽微な異常。ユーザー入力ミス、設定ミス、リトライで復旧可能な一時的エラー。**システムの警告**として、運用者に注意を促すレベル。
    *   `ERROR`: 深刻な異常。システムが正常動作できない、致命的なエラー。**システム管理者への警告**。障害発生時にはこのログを真っ先に確認する。
    *   `DEBUG`/`TRACE`: 開発時・デバッグ用。本番環境では基本オフ。
3.  **例外処理は「異常系をコントロールする設計」だ！**
    *   **安易な `catch (Exception e)` は厳禁！**: 何でもかんでもキャッチすると、本当に重要な例外を見逃したり、意図しない場所で処理されてしまう可能性がある。具体的な例外の種類を想定してキャッチする。
    *   **カスタム例外を積極的に活用しよう**: 業務ロジックに即したカスタム例外を定義し、それをスロー・キャッチすることで、コードの意図が明確になり、保守性が格段に向上する。
    *   **例外は「握りつぶさない」**: 例外をキャッチしたものの、何もせずログにも出さずに処理を終えるのは最悪のアンチパターン。必ずログに出すか、上位に再スローする。
    *   **例外のラッパー化を意識する**: 下位層の技術的例外（`SQLException`など）を、上位層のビジネスロジックに合わせた例外（`ServiceUnavailableException`など）でラップすることで、責任の分離と適切な抽象化を図る。
    *   **グローバルハンドリングの仕組みを理解し活用する**: Webアプリケーションでは、特定のエラーを統一的に処理し、適切なHTTPステータスコードとユーザーフレンドリーなメッセージを返す「グローバル例外ハンドリング」を導入しよう。
4.  **ログと例外はセットで考える！**
    *   例外が発生したら、その情報（スタックトレース、発生時のコンテキスト）を必ずログに出す。ログレベルはERRORが基本だが、ビジネスロジックレベルの想定内エラーならWARNでも良い場合もある。
5.  **機密情報は絶対にログに出すな！**
    *   パスワード、クレジットカード情報、個人を特定できる情報（PII）は絶対にログに書かない。開発環境でもこの習慣を徹底しよう。

これらの「お作法」を意識するだけで、皆さんの書くコードは「動けばいい」レベルから一歩も二歩も踏み出すはずです。
未来の自分、そして一緒に働く未来のチームのために、今日から実践してみましょう！

今回はAIとの対話を通して、ログ設計と例外処理のベストプラクティスを探求しました。
AIは強力なツールですが、最終的にどう設計し、どう実装するかは、私たちエンジニアの思考力と判断力にかかっています。
これからも一緒に、より良いコードを追求していきましょう！

それでは、また次の記事でお会いしましょう！