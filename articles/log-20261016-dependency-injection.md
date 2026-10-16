---
title: "【Log】AIとの対話で学ぶ：依存性注入（DI）"
emoji: "🎓"
type: "tech"
topics: ["java", "csharp", "新人教育", "ai", "思考プロセス"]
published: true
---

みんな、元気にしてるかい？
開発部のシニアエンジニア、〇〇だよ。

最近、「動くコードは書けるけど、なんか保守とかテストがしにくいな…」って悩んでる若手が増えてきた気がするんだ。そんな声を聞くと、「よし、今こそ一歩先の思考を伝授する時だ！」って腕が鳴るってもんだね。

今回は、エンジニアの思考プロセスを解き明かすテーマとして、**「依存性注入（DI）」** を取り上げるよ。難しそうに聞こえるかもしれないけど、これが分かると、君たちの書くコードがグンと洗練されるはずだ。

そして今回は特別に、俺の「AIを活用した思考プロセス」も丸ごと見せちゃおうと思う。AI（今回はGeminiを使ったよ）は、もはや単なるツールじゃない。まるで経験豊富な同僚のように、俺たちの思考を深める手助けをしてくれるんだ。

さあ、骨太なテーマだけど、コーヒー片手に最後まで付き合ってくれると嬉しいな！☕

---

## 1. AIとの対話記録：シニアエンジニアの思考プロセスを覗き見👀

まずは、若手からの相談を受け、俺がどう考え、どうAIに指示を出し、どんなアウトプットを得たか、その一連の流れを追ってみよう。

### 若手からの相談「DIって、正直よく分からないんです…」

先日、若手のA君が俺のところにやってきて、こんな相談をしてきたんだ。

「先輩、お疲れ様です。最近、DI（依存性注入）って言葉をよく聞くんですけど、正直よく分からなくて…。設定ファイルが増えたり、フレームワークを使ったりと、なんか複雑ですよね。単純に`new`しちゃダメなんですか？」

「それに、僕が書いたコードはとりあえず動くんですけど、『テストがしにくい』とか『コードが読み解きにくい』って言われてしまって…。どうすればもっといいコードが書けるようになるんでしょう？」

うんうん、よくある悩みだよね。A君のように「動けばいい」から一歩踏み出したい、でもどうすればいいか分からない、そんな君たちの気持ちは痛いほどよく分かるよ。

### シニアエンジニアの思考「なぜDIが必要なのか、本質から伝えるべき」

A君の悩みを聞いて、俺の頭の中はこんな風に駆け巡った。

1.  **DIへの抵抗感の根源:**
    *   `new`する方がシンプルだと思っている → DIの「メリット」が見えていない。
    *   フレームワークや設定ファイルの複雑さへの懸念 → 「DIコンテナ」と「DIの本質」を混同している。まずは手動DIから理解させるべき。
2.  **A君の現状認識:**
    *   「テストがしにくい」「読み解きにくい」という指摘を受けている → まさにDIが解決する課題だ。ここを重点的に説明しよう。
    *   「動けばいい」から「保守性の高いコード」への意識転換を促したい。
3.  **伝えるべきポイント:**
    *   **DIの「本質」と「目的」を明確にすること。** 単なる技術ではなく、設計思想であることを伝える。
    *   特に「**疎結合**」と「**テスト容易性**」に焦点を当てる。
    *   **具体的なコード例**で示すことで、抽象的な概念を具体化する。
    *   JavaとC#、両方の言語で最新の書き方を取り入れて比較してみよう。
    *   AIに丸投げするのではなく、AIを「思考の壁打ち相手」として活用するプロセス自体を見せることで、若手にも「AI活用術」を伝えたい。

よし、この方針で、まずはAIに基礎的な知識の整理とコード例の叩き台を作ってもらおう。

### AI (Gemini) への指示「DIの本質とメリット、手動DIのコード例を」

俺はGeminiにこんな指示を出したよ。

```text
若手エンジニア向けに、DI（依存性注入）の基本概念とメリット、Java/C#での簡単なコード例を教えてください。

特に「なぜDIが必要なのか」に焦点を当て、具体的に「テストがしやすくなる」という点を強調してください。

DIコンテナは使わず、手動DIの形で見せてください。
Javaは最新のRecordやC#はPrimary Constructorなど、それぞれの言語のモダンな書き方も含めてくれると助かります。

コードは「注文サービスが商品リポジトリに依存する」というシナリオでお願いします。
商品リポジトリはインターフェースとして定義し、そのモック実装と本番実装の両方を示すと、テストのしやすさがより伝わると思います。
```

### AI (Gemini) の回答「DIの本質とコード例」

数秒後、Geminiは期待通りの回答を生成してくれた。

---

#### DI（依存性注入）とは何か？

DI（Dependency Injection：依存性注入）とは、オブジェクトが依存する別のオブジェクトを、そのオブジェクト自身が生成するのではなく、外部から受け取る（注入される）ようにする設計パターンです。

簡単に言えば、「**必要な部品は自分で作らず、誰かから渡してもらう**」という考え方です。

#### なぜDIが必要なのか？ そのメリット

DIを導入する最大の理由は、**コードの「疎結合」を実現し、それによって「テスト容易性」や「変更容易性」を高めること**にあります。

1.  **疎結合（Loose Coupling）:**
    *   オブジェクトが具体的な実装クラスに直接依存しなくなるため、部品同士の結合度が低くなります。
    *   例：「注文サービス」が「商品リポジトリ」を利用する際、特定の実装（例: `JdbcProductRepository`）に直接依存せず、抽象的なインターフェース（例: `ProductRepository`）にのみ依存します。これにより、リポジトリの実装を変更しても、サービス側を修正する必要がなくなります。

2.  **テスト容易性（Testability）:**
    *   これがDIの最も分かりやすいメリットの一つです。特定の外部システム（データベース、外部APIなど）に依存する部分を、テスト時には「モック（模擬）オブジェクト」に差し替えることができます。
    *   これにより、データベース接続なしでサービスのロジックだけを単体テストできるようになり、テストの高速化、安定化、そしてテストコードの記述が容易になります。

3.  **変更容易性（Maintainability / Extensibility）:**
    *   特定のコンポーネントの実装を変更したい場合でも、そのコンポーネントに依存している他のコンポーネントを修正する必要がありません。新しい実装を差し込むだけで対応できます。
    *   例えば、データベースの種類を変更したり、キャッシュ機構を追加したりする際に、依存元のコードに影響を与えずに済みます。

#### JavaでのDI（手動DIの例）

注文サービスが商品リポジトリに依存するシナリオを、Java 21のモダンな書き方（`record`など）で見てみましょう。

```java
// 1. 商品リポジトリのインターフェース
interface ProductRepository {
    Product findById(String productId);
    // 他の操作...
}

// 2. 本番用の商品リポジトリ実装（データベース連携など）
class JdbcProductRepository implements ProductRepository {
    public JdbcProductRepository() {
        // 実際のDB接続などの初期化処理
        System.out.println("JdbcProductRepository が初期化されました。");
    }

    @Override
    public Product findById(String productId) {
        System.out.println("DBから商品ID: " + productId + " を取得します。");
        // 実際のデータベースアクセスロジック
        return new Product(productId, "DB Product " + productId, 1000.0);
    }
}

// 3. テスト用のモック商品リポジトリ実装
class MockProductRepository implements ProductRepository {
    public MockProductRepository() {
        System.out.println("MockProductRepository が初期化されました。");
    }

    @Override
    public Product findById(String productId) {
        System.out.println("モックから商品ID: " + productId + " を取得します。");
        // テスト用のダミーデータを返す
        return new Product(productId, "Mock Product " + productId, 500.0);
    }
}

// 4. 商品を表すレコード（Java 14以降の機能）
record Product(String id, String name, double price) {}

// 5. 注文サービス (DI適用)
class OrderService {
    private final ProductRepository productRepository; // 依存オブジェクト

    // コンストラクタインジェクション: 依存を外部から受け取る
    public OrderService(ProductRepository productRepository) {
        this.productRepository = productRepository;
        System.out.println("OrderService が初期化されました。");
    }

    public void placeOrder(String productId, int quantity) {
        Product product = productRepository.findById(productId);
        if (product == null) {
            throw new IllegalArgumentException("Product not found: " + productId);
        }
        double total = product.price() * quantity;
        System.out.println("注文を作成しました: " + product.name() + " (" + quantity + "個) - 合計: " + total + "円");
        // 注文処理ロジック...
    }
}

// 6. メインメソッド（アプリケーションのエントリポイント）
public class Application {
    public static void main(String[] args) {
        System.out.println("--- 本番環境での実行 ---");
        // 本番用のリポジトリをOrderServiceに注入
        ProductRepository liveRepo = new JdbcProductRepository();
        OrderService liveService = new OrderService(liveRepo);
        liveService.placeOrder("P001", 2);
        System.out.println();

        System.out.println("--- テスト環境での実行（単体テストを想定） ---");
        // テスト用のモックリポジトリをOrderServiceに注入
        ProductRepository testRepo = new MockProductRepository();
        OrderService testService = new OrderService(testRepo);
        testService.placeOrder("P002", 3);
    }
}
```

#### C#でのDI（手動DIの例）

C# 12のPrimary Constructorを活用した例を見てみましょう。

```csharp
using System;

// 1. 商品リポジトリのインターフェース
public interface IProductRepository
{
    Product FindById(string productId);
    // 他の操作...
}

// 2. 本番用の商品リポジトリ実装（データベース連携など）
public class ProductRepository : IProductRepository
{
    public ProductRepository()
    {
        // 実際のDB接続などの初期化処理
        Console.WriteLine("ProductRepository が初期化されました。");
    }

    public Product FindById(string productId)
    {
        Console.WriteLine($"DBから商品ID: {productId} を取得します。");
        // 実際のデータベースアクセスロジック
        return new Product(productId, $"DB Product {productId}", 1000.0);
    }
}

// 3. テスト用のモック商品リポジトリ実装
public class MockProductRepository : IProductRepository
{
    public MockProductRepository()
    {
        Console.WriteLine("MockProductRepository が初期化されました。");
    }

    public Product FindById(string productId)
    {
        Console.WriteLine($"モックから商品ID: {productId} を取得します。");
        // テスト用のダミーデータを返す
        return new Product(productId, $"Mock Product {productId}", 500.0);
    }
}

// 4. 商品を表すレコード（C# 9以降の機能）
public record Product(string Id, string Name, double Price);

// 5. 注文サービス (DI適用) - C# 12 Primary Constructor
public class OrderService(IProductRepository productRepository) // Primary Constructorで依存を宣言
{
    // Primary Constructorで宣言されたパラメータは自動的にフィールドとして利用可能
    // private readonly IProductRepository _productRepository = productRepository; // 明示的にフィールド宣言しなくてもOK (C# 12)

    public void PlaceOrder(string productId, int quantity)
    {
        Console.WriteLine("OrderService が初期化されました。");
        Product product = productRepository.FindById(productId); // Primary Constructorのパラメータを直接使用
        if (product == null)
        {
            throw new ArgumentException($"Product not found: {productId}");
        }
        double total = product.Price * quantity;
        Console.WriteLine($"注文を作成しました: {product.Name} ({quantity}個) - 合計: {total}円");
        // 注文処理ロジック...
    }
}

// 6. メインメソッド（アプリケーションのエントリポイント）
public class Application
{
    public static void Main(string[] args)
    {
        Console.WriteLine("--- 本番環境での実行 ---");
        // 本番用のリポジトリをOrderServiceに注入
        IProductRepository liveRepo = new ProductRepository();
        OrderService liveService = new OrderService(liveRepo);
        liveService.PlaceOrder("P001", 2);
        Console.WriteLine();

        Console.WriteLine("--- テスト環境での実行（単体テストを想定） ---");
        // テスト用のモックリポジトリをOrderServiceに注入
        IProductRepository testRepo = new MockProductRepository();
        OrderService testService = new OrderService(testRepo);
        testService.PlaceOrder("P002", 3);
    }
}
```

---

なるほど、Gemini、素晴らしいアウトプットだ！👏
期待通りの内容で、DIの本質、メリット、そしてJava/C#それぞれのモダンなコード例まで網羅している。

特に「手動DI」に絞って説明してくれたことで、DIコンテナの複雑さに惑わされずに、DIが目指す「疎結合」と「テスト容易性」を具体的にイメージしやすくなったんじゃないかな？

### AIとの対話から見えたこと、そして若手への示唆

AIの回答を見て、俺は改めて若手に伝えたいポイントを整理できた。

*   **「自分で`new`しない」**：これがDIの最も分かりやすい特徴だ。オブジェクトが必要とする依存を、外部から「渡してあげる」という意識が重要。
*   **インターフェースの力**：DIとセットで語られることが多いインターフェースの重要性がよく分かる。具体的な実装ではなく、抽象的な契約に依存することで、モックへの差し替えが容易になるんだ。
*   **テストコードの想像**：モックリポジトリの存在は、「こんな風に単体テストが書けるんだな」という具体的なイメージを与えてくれるはず。

このAIとの対話記録自体が、君たち若手にとって「どうやって新しい技術を学ぶか」「どうやって課題を解決するか」の一つのヒントになったんじゃないかと思うよ。AIは、まさに思考の壁打ち相手として最適だ。

---

## 2. Java vs C#：実装比較から学ぶDIの共通思想と各言語の特色

Geminiが生成してくれたコード例をベースに、JavaとC#それぞれのDIの実装を見ていこう。言語は違えど、DIの思想は共通しているのが分かるはずだ。

### 共通のシナリオ：`OrderService` と `ProductRepository`

どちらの言語でも、**「注文サービス（`OrderService`）が商品情報にアクセスするために商品リポジトリ（`ProductRepository`または`IProductRepository`）に依存する」** というシナリオで説明したね。

そして重要なのは、`OrderService`は**具体的なリポジトリの実装クラス（`JdbcProductRepository`や`ProductRepository`）ではなく、インターフェースに依存している**点だ。

### Java (Java 21) のDI実装

```java
// ProductRepository インターフェース
interface ProductRepository {
    Product findById(String productId);
}

// 本番用実装
class JdbcProductRepository implements ProductRepository { /* ... */ }

// テスト用モック実装
class MockProductRepository implements ProductRepository { /* ... */ }

// OrderService (DI適用)
class OrderService {
    private final ProductRepository productRepository; // インターフェースに依存

    // コンストラクタインジェクション
    public OrderService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    public void placeOrder(String productId, int quantity) {
        // productRepository は外部から注入されたものを使用
        Product product = productRepository.findById(productId);
        // ... 注文処理
    }
}
```

**Java 21 のポイント:**

*   **`record`**: データ保持のためだけのシンプルなクラスを定義するのに最適だね。今回の`Product`レコードのように、イミュータブルなデータクラスを簡潔に書ける。
*   **コンストラクタインジェクション**: Javaでは、依存オブジェクトをコンストラクタの引数として受け取る「コンストラクタインジェクション」が最も一般的で推奨される方法だ。`private final`フィールドとして保持することで、イミュータブルな依存関係を表現できる。

### C# (C# 12) のDI実装

```csharp
// IProductRepository インターフェース
public interface IProductRepository {
    Product FindById(string productId);
}

// 本番用実装
public class ProductRepository : IProductRepository { /* ... */ }

// テスト用モック実装
public class MockProductRepository : IProductRepository { /* ... */ }

// OrderService (DI適用) - C# 12 Primary Constructor
public class OrderService(IProductRepository productRepository) // Primary Constructor
{
    // Primary Constructorで受け取った productRepository は
    // そのままクラススコープで利用可能 (C# 12以降)

    public void PlaceOrder(string productId, int quantity)
    {
        // productRepository は外部から注入されたものを使用
        Product product = productRepository.FindById(productId);
        // ... 注文処理
    }
}
```

**C# 12 のポイント:**

*   **Primary Constructor**: C# 12で導入されたPrimary Constructorは、クラスのコンストラクタ引数を直接クラスのフィールドのように利用できる画期的な機能だ。これにより、コンストラクタで受け取った引数を明示的にフィールドに代入する記述が不要になり、非常に簡潔にDIを実装できる。
*   **`record`**: C#にもJava同様に`record`型があり、データ保持のためのクラスを簡潔に書ける。

### 比較から分かること

*   **DIの原則は不変**: どちらの言語でも「依存するオブジェクトを自分で生成せず、外部から（コンストラクタ経由で）渡してもらう」というDIの根本的な考え方は全く同じだ。
*   **インターフェースの活用**: 疎結合とテスト容易性を実現するために、具体的な実装クラスではなくインターフェースに依存するというプラクティスも共通している。
*   **言語機能の進化**: Javaの`record`やC#のPrimary Constructorのように、新しい言語機能はDIの実装をより簡潔かつ安全に書けるように進化している。それぞれの言語の最新機能に目を向けていくことも、良いコードを書く上で非常に重要だよ。

---

## 3. 若手への一言：明日から使える「お作法」のアドバイス

どうだったかな？ AIとの対話を通して、DIの本質やメリット、そして実際のコード例を見てきたけど、少しは「なるほど！」って思ってくれたら嬉しいな。

最後に、今日から君たちのコードに活かせる「お作法」をいくつかアドバイスするよ。

### ① 「なぜ？」を常に問う

「DIって設定ファイルが増えて複雑だな…」と感じたA君のように、新しい技術に直面した時、まずは「なぜこの技術が必要とされているのか？」と、その**背景や目的**を深く掘り下げてみよう。表面的な使い方だけでなく、その思想を理解することが、真の力になる。

### ② まずは「手動DI」から始める

DIコンテナ（Spring Frameworkや.NET DIなど）は非常に強力だけど、最初は学習コストが高い。今回紹介したように、まずは自分でオブジェクトを生成し、必要な依存をコンストラクタ経由で渡す「手動DI」から始めてみよう。これでDIの基礎的な考え方がしっかり身につくはずだ。

### ③ インターフェースを積極的に使う

「具体的な実装ではなく、抽象的な契約（インターフェース）に依存する」という原則は、DIだけでなく、あらゆる良い設計の基盤となる。インターフェースを定義することで、コードの変更に強く、テストしやすい設計になるから、積極的に活用してほしい。

### ④ 「テストしやすさ」をコードの指標にする

「動けばいい」コードから卒業するための一歩は、**「テストしやすいコードとは何か？」** を意識することだ。DIを導入することで、モックオブジェクトへの差し替えが容易になり、単体テストが格段に書きやすくなる。テストコードを書きながら、「このクラスはテストしやすいか？」という視点を持つことが、設計を洗練させる鍵になるよ。

### ⑤ AIは「思考の壁打ち相手」として活用する

今回見せたように、AIは単に答えを出すだけでなく、君たちの思考を深める強力なパートナーになり得る。疑問に思ったこと、考えたいこと、新しいアイデア、何でもAIにぶつけてみよう。ただし、AIの回答を鵜呑みにせず、常に自分の頭で考え、検証する姿勢は忘れないでくれよ。

---

DIは、単なるプログラミングテクニックではなく、ソフトウェア設計の思想そのものだ。最初は難しく感じるかもしれないけど、この考え方が身につけば、君たちの書くコードは、もっと柔軟に、もっと強く、もっと長く生き続けることができるようになるはずだ。

一歩一歩、着実に成長していこう。応援してるぞ！
また何か困ったことがあったら、いつでも相談しに来てくれ！

それじゃあ、またな！👋