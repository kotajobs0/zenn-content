---
title: "【Log】AIとの対話で学ぶ：REST API設計の基礎"
emoji: "🎓"
type: "tech"
topics: ["java", "csharp", "新人教育", "ai", "思考プロセス"]
published: true
---

皆さん、こんにちは！ 日本を代表するシニアエンジニア（と自称しているベテラン）の〇〇です。
今回から数回にわたって、若手エンジニアの皆さんが「動けばいい」から一歩進んで「保守性の高い、良いコード」を書けるようになるための思考プロセスを、AIとの対話を通じて学んでいくシリーズを始めていきたいと思います。

記念すべき第1回目のテーマは、**「REST API設計の基礎」**です。

最近、若手のA君からこんな相談を受けました。

---

## 1. AIとの対話記録

### 若手からの相談

「〇〇さん、相談いいですか？ 今度、ユーザー情報を管理するAPIを作るタスクをもらったんですけど、先輩のコードを見ても書き方がバラバラで、どう設計すればいいか分からなくて…」

A君は困った顔で、PCの画面を指差します。

「例えば、ユーザー一覧を取得するAPI一つとっても、あるプロジェクトでは `/users` となってて、別のプロジェクトでは `/getUsers` となってたり。ユーザーを登録するAPIも `/createUser` だったり `/users` に POST してたり…一体どれが正解なんですかね？」

「とりあえず動けばいい、とは思うんですけど、後から見返すときに『あれ、このAPIは何だっけ？』ってなることも多くて…」

### シニアエンジニアの思考プロセス

なるほど、A君は「動く」ことはできるけど、「良い設計」とは何か、その指針に悩んでいるんだな。これは若手によくある悩みだ。設計の「お作法」を知らずにやみくもにコードを書いても、将来の自分やチームを苦しめることになる。

特にREST APIは、HTTPという汎用的なプロトコルに乗っかっているからこそ、その「哲学」を理解することが重要だ。URIの設計、HTTPメソッドの使い分け、ステータスコードの意味…。これらを適切に使うことで、APIは自己記述的になり、理解しやすく、そして保守しやすいものになる。

A君の例で言えば、

*   ユーザー一覧取得: `/getUsers` は操作をURIに含めてしまっている。RESTfulでは「リソース」をURIで表現し、そのリソースに対する「操作」はHTTPメソッドで表現するべきだ。つまり、リソースである「複数のユーザー」を指す `/users` に GET するのが適切だろう。
*   ユーザー登録: `/createUser` も同様に操作をURIに含んでいる。リソースである「ユーザー」を新しく作成するのだから、リソースのコレクションである `/users` に POST するのが適切だ。

よし、この基本的な考え方をA君に伝えるとともに、具体的な設計例をAIに作ってもらって、より具体的なイメージを持ってもらおう。AIなら最新のプラクティスに基づいた、一貫性のある回答を出してくれるはずだ。

### AI (Gemini) への指示

「よし、A君。今、君が悩んでいる『REST APIの設計』について、私が普段AIを使う時のように、一緒に考えてみようか。」

「Gemini、以下の要件でRESTfulなAPI設計の基礎を教えてください。具体的には、ユーザー情報を管理するCRUD操作（作成、読み取り、更新、削除）について、適切なURI、HTTPメソッド、リクエスト/レスポンスのJSON例、およびHTTPステータスコードを提示してください。また、その設計に基づいたJava (Spring Boot) とC# (ASP.NET Core) のシンプルな実装例も合わせて提供してください。各言語の最新機能（Java 21 / C# 12）を活用した簡潔な書き方を期待します。」

### AI (Gemini) の回答

かしこまりました。RESTful APIの設計基礎と、Java (Spring Boot)、C# (ASP.NET Core) における実装例についてご説明します。

---

#### **RESTful API設計の原則**

RESTful APIは、以下の原則に基づいて設計されます。

1.  **リソース指向**: URIは操作ではなく、リソース（名詞）を表現します。
2.  **ステートレス**: 各リクエストは独立しており、サーバーはクライアントの状態を保持しません。
3.  **クライアント/サーバー分離**: UIとAPIが分離され、それぞれ独立して進化できます。
4.  **統一インターフェース**: HTTPメソッド（GET, POST, PUT, DELETEなど）で操作を表現し、URIはリソースを一意に特定します。

#### **ユーザー情報管理APIの設計例**

ここでは、`User` リソースを管理するAPIを例に説明します。

**リソース**: `User`

| 操作（CRUD）     | HTTPメソッド | URI例                    | リクエストボディ (JSON)              | レスポンスボディ (JSON)              | ステータスコード | 備考                                         |
| :--------------- | :----------- | :----------------------- | :----------------------------------- | :----------------------------------- | :--------------- | :------------------------------------------- |
| **ユーザー一覧取得** | `GET`        | `/api/users`             | (なし)                               | `[{ "id": 1, "name": "Alice" }, ...]` | `200 OK`         | 全ユーザー情報を取得                         |
| **特定ユーザー取得** | `GET`        | `/api/users/{id}`        | (なし)                               | `{ "id": 1, "name": "Alice" }`       | `200 OK`         | `id`で指定されたユーザーを取得。見つからなければ`404 Not Found` |
| **ユーザー作成**     | `POST`       | `/api/users`             | `{ "name": "Bob", "email": "..." }`  | `{ "id": 2, "name": "Bob", ... }`    | `201 Created`    | 新規ユーザー作成。作成されたリソースのURIを`Location`ヘッダーに含む |
| **ユーザー更新**     | `PUT`        | `/api/users/{id}`        | `{ "name": "Charlie", "email": "..."}` | `{ "id": 1, "name": "Charlie", ... }`| `200 OK`         | `id`で指定されたユーザーを更新。リソースが存在しない場合は`404 Not Found` |
| **ユーザー部分更新** | `PATCH`      | `/api/users/{id}`        | `{ "name": "David" }`                | `{ "id": 1, "name": "David", ... }`  | `200 OK`         | `id`で指定されたユーザーの一部を更新。`PUT`との違いは、リソース全体ではなく一部を更新する際に使用 |
| **ユーザー削除**     | `DELETE`     | `/api/users/{id}`        | (なし)                               | (なし)                               | `204 No Content` | `id`で指定されたユーザーを削除。削除対象がない場合は`404 Not Found` |

---

## 2. Java vs C# 実装比較

さて、AIが出してくれたこの設計を、Java (Spring Boot) と C# (ASP.NET Core) で実際にどのように実装するか見ていきましょう。
最新の言語機能も交えて、できるだけ簡潔に書く方法を紹介します。

### 前提

*   **Java**: Spring Boot 3.x, Java 21 を想定。
*   **C#**: ASP.NET Core 8.x, C# 12 を想定。

### データ転送オブジェクト (DTO) の定義

まずは、APIでやり取りするユーザー情報を表現するDTO（Data Transfer Object）を定義します。

#### Java (Java 21: record)

Java 21では、`record`が非常に簡潔にDTOを定義できます。イミュータブル（不変）なデータクラスとして最適です。

```java
// src/main/java/com/example/demo/domain/User.java
package com.example.demo.domain;

// レスポンス用DTO (id, name, emailを持つ)
public record UserResponse(Long id, String name, String email) {
    // recordは自動的にコンストラクタ、equals(), hashCode(), toString() を生成
}

// リクエスト用DTO (name, emailを持つ)
public record UserRequest(String name, String email) {
}
```

#### C# (C# 12: record class / primary constructor)

C# 12では、`record class` または `class` に `primary constructor` を使うことで、Javaのrecordと同様に簡潔にDTOを定義できます。

```csharp
// Models/User.cs
namespace ApiDemo.Models;

// レスポンス用DTO (id, name, emailを持つ)
public record UserResponse(int Id, string Name, string Email);

// リクエスト用DTO (name, emailを持つ)
// record classでも良いが、mutableなDTOなら通常のclass + primary constructorも有効
public class UserRequest(string Name, string Email);
```

### コントローラーの実装

次に、AIが提示した設計に基づいて、APIのエンドポイントを実装します。ここでは、簡略化のためインメモリのリストをデータストアとして使います。

#### Java (Spring Boot)

`@RestController` アノテーションを使って、RESTful APIのコントローラーを定義します。

```java
// src/main/java/com/example/demo/api/UserController.java
package com.example.demo.api;

import com.example.demo.domain.UserRequest;
import com.example.demo.domain.UserResponse;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

@RestController
@RequestMapping("/api/users") // ベースURIを定義
public class UserController {

    // 簡易的なデータストア（インメモリ）
    private final Map<Long, UserResponse> users = new ConcurrentHashMap<>();
    private final AtomicLong idCounter = new AtomicLong();

    public UserController() {
        // 初期データ
        users.put(idCounter.incrementAndGet(), new UserResponse(1L, "Alice", "alice@example.com"));
        users.put(idCounter.incrementAndGet(), new UserResponse(2L, "Bob", "bob@example.com"));
    }

    /**
     * GET /api/users - ユーザー一覧取得
     */
    @GetMapping
    public List<UserResponse> getAllUsers() {
        return new ArrayList<>(users.values());
    }

    /**
     * GET /api/users/{id} - 特定ユーザー取得
     */
    @GetMapping("/{id}")
    public UserResponse getUserById(@PathVariable Long id) {
        return Optional.ofNullable(users.get(id))
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found with id: " + id));
    }

    /**
     * POST /api/users - ユーザー作成
     */
    @PostMapping
    @ResponseStatus(HttpStatus.CREATED) // 201 Created を返す
    public UserResponse createUser(@RequestBody UserRequest userRequest) {
        Long newId = idCounter.incrementAndGet();
        UserResponse newUser = new UserResponse(newId, userRequest.name(), userRequest.email());
        users.put(newId, newUser);
        return newUser;
    }

    /**
     * PUT /api/users/{id} - ユーザー更新
     * 全てのフィールドを更新する想定
     */
    @PutMapping("/{id}")
    public UserResponse updateUser(@PathVariable Long id, @RequestBody UserRequest userRequest) {
        if (!users.containsKey(id)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found with id: " + id);
        }
        UserResponse updatedUser = new UserResponse(id, userRequest.name(), userRequest.email());
        users.put(id, updatedUser); // 既存のユーザーを上書き
        return updatedUser;
    }

    /**
     * DELETE /api/users/{id} - ユーザー削除
     */
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT) // 204 No Content を返す
    public void deleteUser(@PathVariable Long id) {
        if (users.remove(id) == null) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "User not found with id: " + id);
        }
    }
}
```

#### C# (ASP.NET Core)

`[ApiController]` と各HTTPメソッドに対応するアノテーション（`[HttpGet]`, `[HttpPost]` など）を使ってコントローラーを定義します。

```csharp
// Controllers/UsersController.cs
using ApiDemo.Models;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Concurrent;

namespace ApiDemo.Controllers;

[ApiController]
[Route("api/[controller]")] // ベースURIを定義。クラス名から"Controller"を除いた部分が使われる -> /api/users
public class UsersController : ControllerBase
{
    // 簡易的なデータストア（インメモリ）
    private static readonly ConcurrentDictionary<int, UserResponse> _users = new();
    private static int _nextId = 0;

    static UsersController()
    {
        // 初期データ
        _users.TryAdd(Interlocked.Increment(ref _nextId), new UserResponse(1, "Alice", "alice@example.com"));
        _users.TryAdd(Interlocked.Increment(ref _nextId), new UserResponse(2, "Bob", "bob@example.com"));
    }

    /**
     * GET /api/users - ユーザー一覧取得
     */
    [HttpGet]
    public ActionResult<IEnumerable<UserResponse>> GetAllUsers()
    {
        return Ok(_users.Values.ToList());
    }

    /**
     * GET /api/users/{id} - 特定ユーザー取得
     */
    [HttpGet("{id}")] // パスパラメータを定義
    public ActionResult<UserResponse> GetUserById(int id)
    {
        if (_users.TryGetValue(id, out var user))
        {
            return Ok(user);
        }
        return NotFound($"User not found with id: {id}");
    }

    /**
     * POST /api/users - ユーザー作成
     */
    [HttpPost]
    public ActionResult<UserResponse> CreateUser([FromBody] UserRequest userRequest) // [FromBody] でリクエストボディをバインド
    {
        var newId = Interlocked.Increment(ref _nextId);
        var newUser = new UserResponse(newId, userRequest.Name, userRequest.Email);
        _users.TryAdd(newId, newUser);
        // 201 Created を返し、Locationヘッダーに新規リソースのURIを含める
        return CreatedAtAction(nameof(GetUserById), new { id = newId }, newUser);
    }

    /**
     * PUT /api/users/{id} - ユーザー更新
     * 全てのフィールドを更新する想定
     */
    [HttpPut("{id}")]
    public ActionResult<UserResponse> UpdateUser(int id, [FromBody] UserRequest userRequest)
    {
        if (!_users.ContainsKey(id))
        {
            return NotFound($"User not found with id: {id}");
        }
        var updatedUser = new UserResponse(id, userRequest.Name, userRequest.Email);
        _users.AddOrUpdate(id, updatedUser, (key, existingVal) => updatedUser); // 既存のユーザーを上書き
        return Ok(updatedUser);
    }

    /**
     * DELETE /api/users/{id} - ユーザー削除
     */
    [HttpDelete("{id}")]
    public ActionResult DeleteUser(int id)
    {
        if (_users.TryRemove(id, out _))
        {
            return NoContent(); // 204 No Content を返す
        }
        return NotFound($"User not found with id: {id}");
    }
}
```

---

## 3. 若手への一言：明日から使える「お作法」のアドバイス

A君、どうだったかな？ AIとの対話と実際のコードを見て、少しはREST API設計のイメージが湧いただろうか。

今回紹介したRESTfulな設計は、単に「動けばいい」以上の価値を生み出すんだ。

*   **誰が見ても分かりやすいAPIになる。**
*   **将来の機能追加や変更に強い構造になる。**
*   **クライアントとサーバー間の認識齟齬が減り、連携がスムーズになる。**

これはまさに、僕たちが目指す「保守性の高いコード」の第一歩なんだ。
明日から君が実践できる「お作法」をいくつかアドバイスするよ。

1.  **URIは「名詞」で「リソース」を表現する**:
    *   `GET /users` (ユーザー一覧)
    *   `GET /users/{id}` (特定のユーザー)
    *   `POST /users` (ユーザー作成)
    *   決して `GET /getUsers` や `POST /createUser` のように「操作動詞」をURIに入れないこと。
2.  **HTTPメソッドで「操作」を明確にする**:
    *   `GET`: リソースの取得（参照系）
    *   `POST`: 新しいリソースの作成（登録系）
    *   `PUT`: リソースの全更新（更新系）
    *   `DELETE`: リソースの削除（削除系）
    *   それぞれのメソッドが持つ「べき」意味を理解し、それに従って使い分けること。特に、`GET`は何度実行しても結果が変わらない「冪等性」があるべきだ、という原則も頭の片隅に置いておくと良い。
3.  **適切なHTTPステータスコードを返す**:
    *   `200 OK`: 成功（GET, PUTなど）
    *   `201 Created`: 新規作成成功（POST）
    *   `204 No Content`: 削除成功など、レスポンスボディがない場合（DELETE）
    *   `400 Bad Request`: クライアント側のリクエストエラー
    *   `404 Not Found`: リソースが見つからない
    *   `500 Internal Server Error`: サーバー側の予期せぬエラー
    *   これにより、クライアント側はAPIの実行結果を明確に判断できる。
4.  **コードの書き方を統一する**:
    *   プロジェクト内で、DTOの命名規則、コントローラーの構造などをメンバー間で合意し、統一する。今回紹介した`record`や`primary constructor`のような最新機能も、うまく使えばコードを簡潔に、かつ意図を明確にできる。
5.  **他人のコードを読む、そして議論する**:
    *   一人で抱え込まず、先輩のコードを読み、疑問に思ったことは積極的に質問しよう。そして、自分の設計について「なぜそうしたのか」を説明できるように議論する機会を持つこと。それが一番の学びになる。

最初から完璧な設計は難しい。でも、今回学んだ「RESTfulの基本原則」を意識して、実際に手を動かし、試行錯誤することで、君のコードは着実にレベルアップしていくはずだ。

「とりあえず動けばいい」フェーズは卒業！ 次は「保守性の高い、良い設計」を目指して、一緒に頑張っていこう！

それでは、また次回！