---
title: "【Log】AIとの対話で学ぶ：コードレビューの作法"
emoji: "🎓"
type: "tech"
topics: ["java", "csharp", "新人教育", "ai", "思考プロセス"]
published: true
---

皆さん、こんにちは！ 日本を代表する、かどうかはさておき（笑）、この道ン十年、システムと格闘し続けてきたシニアエンジニアです。Zennでは、若手の皆さんが「動けばいい」から一歩先の「保守性の高いコード」を書けるようになるための思考プロセスを、私の経験と現代の強力なパートナーAIとの対話を通して伝えていければと思っています。

今回のテーマは、エンジニアの成長に不可欠な「**コードレビューの作法**」です。

皆さんはコードレビューに対してどんなイメージを持っていますか？
「指摘されるのが怖い」「どうレビューすればいいか分からない」「結局、自分のコードって何がダメなの？」なんて思っているかもしれませんね。

大丈夫、私も若い頃はそうでした。しかし、コードレビューは決してネガティブなものではありません。むしろ、チーム全体の生産性を高め、個々のエンジニアを成長させるための、最も強力な学習ツールなのです。

今回は、若手エンジニアからのよくある悩みをAI（Gemini）にぶつけ、その回答からJavaとC#の最新機能を交えつつ、具体的なコード例で「保守性の高いコード」へのステップアップを一緒に考えていきましょう。

## 1. AIとの対話記録

### 若手からの相談

ある日、元気のない若手社員が私のところにやってきました。

「先輩、実はコードレビューのことで悩んでいます…。いつも『もっと保守的に』とか『可読性を上げて』とか指摘されるんですが、具体的にどうすればいいのか、なかなかピンとこなくて。なぜ自分のコードが指摘されるのか、どうすれば良いコードが書けるようになるんでしょうか？」

### シニアのあなたの思考

うんうん、よくある悩みだね。レビューは単なるバグ探しじゃなく、チーム全体の知識を共有し、コード品質を高めるための大切なプロセスなんだ。君がどういう視点でコードを書けば、レビューで指摘されにくくなるか、また、どういう視点でレビューすれば質の高いレビューができるか、AIと一緒に考えてみようか。Gemini、助けてくれ。

### AI (Gemini) への指示

「あなたは経験豊富なJava/C#のシニアエンジニアです。若手エンジニア（入社1-3年目）がコードレビューで指摘されがちな点、および保守性・可読性を高めるための具体的な改善策について、最新のJava (21) と C# (12) の機能も踏まえながら解説してください。特に、DTOのマッピングや不変オブジェクトの扱い方、エラーハンドリングに焦点を当ててください。レビューする側がどのような視点を持つべきかについてもアドバイスをお願いします。」

### AIの回答

AIは瞬時に、以下のような構造化されたアドバイスを提示してくれました。

---
若手エンジニアの皆さん、コードレビューでの指摘は、決して個人攻撃ではありません。それは、あなたのコードをより良くするための貴重なフィードバックであり、チーム全体の成長のための機会です。

コードレビューで指摘されがちな点と、それを改善するための思考プロセスを、Java 21とC# 12の最新機能も交えながら解説します。

#### 1. 指摘されがちな点と背景

1.  **命名規則の不統一・不明確さ**:
    *   `data`、`temp`、`list`など、汎用的すぎて意図が読み取れない変数名・メソッド名。
    *   背景: コードの意図が不明瞭になり、読み解くのに時間がかかる。
2.  **マジックナンバー・マジック文字列の散見**:
    *   コード中に数値リテラル（例: `if (status == 1)`) や文字列リテラル（例: `if (type == "ADMIN")`) が直接埋め込まれている。
    *   背景: 数値や文字列の意味が不明。変更があった場合に修正箇所が多くなり、ミスを誘発する。
3.  **DRY (Don't Repeat Yourself) 原則の違反**:
    *   同じような処理が複数の箇所にコピー＆ペーストされている。
    *   背景: 修正が必要な場合に全箇所を修正しなければならず、漏れや不整合の原因となる。
4.  **単一責任原則 (Single Responsibility Principle) の違反**:
    *   一つのクラスやメソッドが、複数の異なる責任（目的）を担っている。
    *   背景: 変更の影響範囲が広くなり、デバッグが困難になる。再利用性も低下する。
5.  **エラーハンドリングの不適切さ**:
    *   例外を単に`catch`して何も処理しない (`catch (Exception e) {}`)。
    *   広すぎる例外をキャッチしている (`catch (Exception e)`)。
    *   適切なログ出力がない、あるいは不十分。
    *   背景: エラーが発生しても検知できず、原因究明が困難になる。システム全体の信頼性が損なわれる。
6.  **不変性の欠如**:
    *   DTO（Data Transfer Object）などのデータ保持クラスが可変で、意図しない場所で状態が変更される可能性がある。
    *   背景: スレッドセーフティの問題や、デバッグが非常に困難な副作用を引き起こす可能性がある。
7.  **最新の言語機能の不活用**:
    *   古い書き方でコードが冗長になっている。
    *   背景: コードが長くなり、可読性が低下する。コンパイラの最適化の恩恵を受けられない場合もある。

#### 2. 保守性・可読性を高める改善策とレビュー観点

##### a. DTOのマッピングと不変オブジェクトの扱い方

*   **課題**: 手動でのプロパティ設定は冗長でミスが発生しやすい。DTOが可変だと、どこで値が変わったか追跡が困難になる。
*   **改善策**:
    *   **不変オブジェクトの採用**: データ保持専用のクラスは、一度生成されたら状態が変更できない「不変（Immutable）」にするのが基本です。
        *   **Java 21**: `record`クラスを積極的に活用しましょう。コンストラクタ、getter、`equals`/`hashCode`/`toString`が自動生成され、非常に簡潔に不変クラスを定義できます。
        *   **C# 12**: `record class`または`record struct`を利用します。`init`アクセサーを持つプロパティと組み合わせることで、初期化時のみ値を設定できる不変プロパティを持つクラスを簡単に作成できます。また、C# 9以降の`with`式を使うことで、不変オブジェクトの一部を変更した新しいインスタンスを簡潔に生成できます。
    *   **マッピングライブラリの活用**:
        *   手動マッピングは極力避け、JavaならMapStruct、C#ならAutoMapperのようなマッピングライブラリの導入を検討しましょう。定型的なマッピングコードを自動生成/自動実行してくれます。
*   **レビュー観点**:
    *   データ保持クラスは`record`型や`init`アクセサーを持つ不変オブジェクトになっているか？
    *   データマッピングは冗長になっていないか？ ライブラリの導入やヘルパーメソッドによる集約を検討できないか？
    *   DTOのプロパティ名はそのデータの意味を正確に表現しているか？

##### b. エラーハンドリング

*   **課題**: エラーを無視したり、広すぎる例外をキャッチしたりすると、問題発生時に対応が遅れる。
*   **改善策**:
    *   **具体的な例外をキャッチ**: `Exception`のような汎用的な例外ではなく、`IOException`や`SQLException`など、発生しうる具体的な例外をキャッチしましょう。
    *   **適切なログ出力**: 例外発生時は、スタックトレースを含め、何が、どこで、なぜ発生したのかが分かるようにログを出力しましょう。
    *   **回復可能性の判断**:
        *   回復可能なエラーであれば、代替処理や再試行を実装。
        *   回復不可能なエラーであれば、適切なメッセージと共に上位に例外を再スローするか、アプリケーションを終了させるかを検討。
    *   **Null安全性の確保**:
        *   **Java**: `Optional`クラスを使い、nullの可能性を明示的に表現し、チェーンメソッドで安全に処理しましょう。
        *   **C#**: Nullable Reference Types (C# 8.0以降) を活用し、コンパイラによるnullチェックの恩恵を受けましょう。`?`演算子によるnull条件演算子も活用できます。
*   **レビュー観点**:
    *   例外が不適切に無視されていないか？
    *   広すぎる例外（`Exception`）をキャッチしてしまっていないか？
    *   エラー発生時に、デバッグに必要な情報（スタックトレース、関連データ）がログに出力されるか？
    *   nullの可能性のある値は安全に扱われているか？ (`Optional`やNullable Reference Typesの活用状況)

##### c. 最新言語機能の活用 (Java 21 / C# 12)

*   **課題**: 最新の書き方を知らず、冗長なコードを書いてしまう。
*   **改善策**:
    *   **Java 21**:
        *   **Pattern Matching for `switch`**: `instanceof`とキャストの組み合わせを簡潔に表現。
        *   **Record Patterns**: `record`のコンポーネントをパターンマッチングで直接抽出。
        *   **Virtual Threads (Project Loom)**: スレッドのオーバーヘッドを削減し、高並行処理を簡潔に記述。
    *   **C# 12**:
        *   **Primary Constructors**: クラス定義と同時にコンストラクタ引数を宣言し、フィールドやプロパティの初期化に利用可能。特にDIコンテナを使う場合に簡潔に書ける。
        *   **Collection Expressions**: コレクションの初期化をより簡潔に記述。
        *   **Pattern Matching**: `switch`式や`is`演算子、`when`句などを使った柔軟なパターンマッチング。
*   **レビュー観点**:
    *   冗長なコードを最新の言語機能で置き換えられないか？ (例: `if-else if-else`の羅列を`switch`式/パターンマッチングで置き換えられないか？)
    *   コードの意図がより明確になるような新機能の使い方はあるか？

---

## 2. Java vs C# 実装比較：不変オブジェクトとパターンマッチング

AIの回答で「不変オブジェクト」と「最新機能の活用」が挙がりましたね。これらはコードの保守性と可読性を高める上で非常に重要な要素です。
ここでは、データ転送オブジェクト (DTO) の不変性と、それらを扱う際のパターンマッチングについて、JavaとC#の最新機能を交えて比較してみましょう。

### シナリオ：商品情報を扱うDTOと、その種別による処理

とあるECサイトで、商品情報を表すDTOと、その商品の価格帯によって異なる処理を行うメソッドを考えます。

#### Java (21) での実装

Java 21では、`record`型や`switch`式とパターンマッチングが進化し、データクラスや条件分岐を非常に簡潔に記述できるようになりました。

```java
// ProductDtoをrecordで定義 (不変オブジェクト)
// コンストラクタ、getter、equals/hashCode/toStringが自動生成される
public record ProductDto(String id, String name, int price) {
    // コンストラクタにカスタム検証を追加することも可能
    public ProductDto {
        if (price < 0) {
            throw new IllegalArgumentException("Price cannot be negative");
        }
    }
}

public class ProductService {

    // 使用例: ProductDtoのインスタンス生成
    public ProductDto createLaptop() {
        return new ProductDto("P001", "Laptop", 120000);
    }

    public ProductDto createMouse() {
        return new ProductDto("P002", "Mouse", 3000);
    }

    // 商品の価格帯に応じてカテゴリを判定 (Switch式とパターンマッチング)
    public String getProductCategory(ProductDto product) {
        return switch (product) {
            case ProductDto p when p.price() >= 100000 -> "High-end Product";
            case ProductDto p when p.price() >= 50000 -> "Mid-range Product";
            case ProductDto p -> "Standard Product"; // それ以外のProductDto
        };
    }

    // より汎用的なパターンマッチングの例
    public String getItemDescription(Object item) {
        return switch (item) {
            case ProductDto p -> "Product: " + p.name() + " (ID: " + p.id() + ")";
            case String s -> "String data: " + s;
            case Integer i -> "Integer value: " + i;
            default -> "Unknown item type";
        };
    }

    public static void main(String[] args) {
        ProductService service = new ProductService();
        ProductDto laptop = service.createLaptop();
        ProductDto mouse = service.createMouse();

        System.out.println("Laptop Category: " + service.getProductCategory(laptop)); // High-end Product
        System.out.println("Mouse Category: " + service.getProductCategory(mouse));   // Standard Product

        System.out.println(service.getItemDescription(laptop)); // Product: Laptop (ID: P001)
        System.out.println(service.getItemDescription("Hello Zenn")); // String data: Hello Zenn
        System.out.println(service.getItemDescription(123)); // Integer value: 123
    }
}
```

#### C# (12) での実装

C# 12でも、`record class`や`primary constructor`、拡張されたパターンマッチングが利用できます。

```csharp
// ProductDtoをrecord classで定義 (不変オブジェクト)
// プロパティはinitアクセサーを持つため、初期化後変更不可
public record ProductDto(string Id, string Name, int Price)
{
    // コンストラクタにカスタム検証を追加することも可能
    public ProductDto(string id, string name, int price) : this(id, name, price)
    {
        if (price < 0)
        {
            throw new ArgumentException("Price cannot be negative");
        }
    }
}

public class ProductService
{
    // 使用例: ProductDtoのインスタンス生成
    public ProductDto CreateLaptop()
    {
        return new ProductDto("P001", "Laptop", 120000);
    }

    public ProductDto CreateMouse()
    {
        return new ProductDto("P002", "Mouse", 3000);
    }

    // 商品の価格帯に応じてカテゴリを判定 (パターンマッチング)
    public string GetProductCategory(ProductDto product) => product switch
    {
        { Price: >= 100000 } p => "High-end Product", // プロパティパターン
        { Price: >= 50000 } p => "Mid-range Product",
        _ => "Standard Product" // それ以外のProductDto
    };

    // Primary Constructorの利用例 (C# 12)
    // コンストラクタ引数で直接依存性を注入し、フィールドとして利用できる
    public class ProductAnalyzer(ILogger logger) // loggerがprivate readonlyフィールドとして扱われる
    {
        public void Analyze(ProductDto product)
        {
            logger.LogInformation($"Analyzing product: {product.Name}");
            // ... 解析処理 ...
        }
    }

    // より汎用的なパターンマッチングの例
    public string GetItemDescription(object item) => item switch
    {
        ProductDto p => $"Product: {p.Name} (ID: {p.Id})",
        string s => $"String data: {s}",
        int i => $"Integer value: {i}",
        _ => "Unknown item type" // _ はdiscard pattern
    };

    public static void Main(string[] args)
    {
        ProductService service = new ProductService();
        ProductDto laptop = service.CreateLaptop();
        ProductDto mouse = service.CreateMouse();

        Console.WriteLine($"Laptop Category: {service.GetProductCategory(laptop)}"); // High-end Product
        Console.WriteLine($"Mouse Category: {service.GetProductCategory(mouse)}");   // Standard Product

        Console.WriteLine(service.GetItemDescription(laptop)); // Product: Laptop (ID: P001)
        Console.WriteLine(service.GetItemDescription("Hello Zenn")); // String data: Hello Zenn
        Console.WriteLine(service.GetItemDescription(123)); // Integer value: 123

        // ProductAnalyzer analyzer = new ProductAnalyzer(new ConsoleLogger()); // ILoggerはモック
        // analyzer.Analyze(laptop);
    }

    // ILoggerの簡易実装（Primary Constructorの例のため）
    public interface ILogger { void LogInformation(string message); }
    public class ConsoleLogger : ILogger { public void LogInformation(string message) => Console.WriteLine(message); }
}
```

### 比較と考察

*   **不変DTO**:
    *   Javaの`record`とC#の`record class`は、どちらもデータ保持に特化した不変クラスを非常に簡潔に定義できます。これにより、意図しない値の変更によるバグを防ぎ、スレッドセーフなコードを書きやすくなります。
    *   C#の`record class`は`with`式によるコピーコンストラクタ的な機能も提供し、元のインスタンスを壊さずに一部プロパティだけ変更した新しいインスタンスを簡単に作れます。Javaではこれに相当する機能は提供されていませんが、BuilderパターンやLombokなどのライブラリで代替できます。
*   **パターンマッチング**:
    *   両言語とも`switch`文（Javaの`switch`式、C#の`switch`式）が進化し、オブジェクトの型やプロパティの値に応じた柔軟な分岐処理を簡潔に記述できるようになりました。これにより、複雑な`if-else if`の連鎖が減り、可読性が向上します。
*   **C# 12のPrimary Constructor**:
    *   C# 12のPrimary Constructorは、依存性注入（DI）など、コンストラクタ引数をクラス内でフィールドとして利用するケースで、クラス定義をさらに簡潔にする強力な機能です。Javaの`record`コンストラクタとは異なり、普通のクラスにも適用できます。

このように、両言語とも「より簡潔に、より安全に、より意図を明確に」コードを書くための機能が進化しています。これらの新機能を適切に活用することが、「保守性の高いコード」への第一歩となります。

## 3. 若手への一言：明日から使える「お作法」

さて、AIとの対話と具体的なコード比較を通して、コードレビューの重要性と、良いコードを書くための具体的なヒントが見えてきたと思います。最後に、明日から皆さんが実践できる「コードレビューのお作法」を、レビューする側・される側の両方に向けてお伝えします。

### レビューを受ける君へ

指摘は「コード」へのものであり、「人」へのものではありません。この心構えが一番大切です。

1.  **オープンな心で受け止めるべし**: 指摘はあなたの成長のチャンスです。感情的にならず、まずは「なるほど、そういう視点もあるのか」と受け止めてみましょう。
2.  **感謝の気持ちを伝えるべし**: レビューは時間と労力のかかる作業です。コメントをもらったら「レビューありがとうございます！」と一言添えるだけで、次のレビューが建設的なものになります。
3.  **なぜ指摘されたのか、本質を理解しようと努めるべし**: 「こう直せ」という指示だけでなく、「なぜそう直すべきなのか」その背景や意図を考えましょう。分からなければ積極的に質問してください。これが一番の学びになります。
4.  **自分で代替案を考え、質問としてぶつけるべし**: 指摘された点に対して、「こう直すのはどうでしょうか？」「こういう意図でこの書き方をしたのですが、より良い方法はありますか？」と自分の考えを添えて質問してみましょう。能動的な姿勢は、レビュワーに良い印象を与え、より深い議論に繋がります。
5.  **疑問は溜め込まず、すぐに質問するべし**: コードレビューツール上でのコメントのやり取りだけでなく、直接口頭で質問するのも有効です。文章だけでは伝わりにくいニュアンスも理解できます。

### レビューをする君へ

レビューは「バグ探しゲーム」ではありません。チームのコード品質とメンバーの成長を促す「対話」です。

1.  **まずはPR Descriptionを熟読すべし**: プルリクエストの目的、変更範囲、実装方針を理解してからコードを見始めましょう。レビュイーの意図を把握せずに行うレビューは、的外れになりがちです。
2.  **最初に良い点を褒めるべし（心理的安全性）**: 「ここ、綺麗に書けているね！」「この考慮漏れがないのは素晴らしい！」など、良い点を見つけて最初にコメントしましょう。これにより、レビュイーは安心して次の指摘を受け入れやすくなります。
3.  **「〜すべき」ではなく、「〜するとより良い」と提案形式で**: 「ここを直せ」ではなく、「ここを`record`にすると、より不変性が保証されて保守性が高まりそうだね」のように、理由を添えて提案しましょう。
4.  **指摘は具体的で代替案（ヒント）を示すべし**: 「可読性が低い」だけでは伝わりません。「このメソッドは複数の処理をしているから、`X`と`Y`の二つに分けると単一責任が保てて分かりやすくなるよ」のように、具体的なコード例や改善の方向性を示しましょう。
5.  **レビューのスコープを絞るべし**: 一度のプルリクエストで完璧なコードを求めるのは現実的ではありません。主要な目的が達成されているか、大きなバグや設計の問題はないか、チームのコーディング規約に反していないかなど、優先順位をつけてレビューしましょう。完璧主義は、レビューを停滞させます。
6.  **完璧なコードは存在しないと心得るべし**: レビュワー自身の主観や好みで指摘しすぎていないか、立ち止まって考えましょう。チームの合意形成されたコーディング規約や設計原則に則っているかを基準にすることが重要です。

---

コードレビューは、チームでより良いプロダクトを作り、エンジニアとして成長するための最も強力なツールの一つです。AIは強力な相棒ですが、最終的に判断し、責任を持つのは私たち人間です。

「動けばいい」という段階を卒業し、一歩先の「保守性、可読性、拡張性を意識したコード」を書くことを、ぜひ楽しんでください。そして、コードレビューを通じてチームメンバーと切磋琢磨し、最高のプロダクトを一緒に作り上げていきましょう！

それでは、また次回の記事で！