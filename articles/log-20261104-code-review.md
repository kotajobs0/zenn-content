---
title: "【Log】AIとの対話で学ぶ：コードレビューの作法"
emoji: "🎓"
type: "tech"
topics: ["java", "csharp", "新人教育", "ai", "思考プロセス"]
published: true
---

皆さん、こんにちは！
日本を代表するシニアエンジニアの〇〇です。今日は、若手エンジニアの皆さんがぶつかりやすい壁の一つ、「コードレビューの作法」について、僕自身の思考プロセス、そして最新のAIを交えながら深掘りしていこうと思います。

「動けばいい」という段階から一歩進んで、「保守性の高いコード」を書くためのヒントを掴んでほしい。そして、コードレビューが皆さんの成長を加速させる最高の場であると実感してもらえたら嬉しいです。

## 1. AIとの対話記録：シニアエンジニアの思考プロセス

まずは、僕が普段どのように課題を捉え、解決策を考えるか、その思考プロセスをAIとの対話記録としてお見せしましょう。

### 若手からの相談

ある日、若手エンジニアの彼が、少し浮かない顔で相談に来ました。

「先輩、相談があるんですが…」
「最近、コードレビューで指摘が多くて、どうしたらいいか悩んでいます。先輩が書いたコードはいつもスマートで、どうしてこんな書き方ができるんだろうって。自分のは、動くは動くんですけど、レビューで『ここはもっとこうした方が良い』とか、『この設計だと将来的に辛い』とか言われることが多くて…正直、何が良くて何がダメなのか、具体的な指針が見えなくて戸惑っています。」
「あと、指摘されるのがちょっと怖くて、レビューに出すのが億劫になる時もあります…。」

### シニアのあなたの思考

彼の悩み、うんうん、よくわかる。僕も通ってきた道だ。
「動けばいい」という段階から、「保守性」「拡張性」「可読性」といった品質の高いコードを目指すのは、一筋縄ではいかない。経験と知識が求められる。
特にコードレビューは、技術的な指導の場であると同時に、コミュニケーションの場でもある。彼が「怖い」と感じているのは、レビューの本質をまだ掴みきれていない証拠だろう。

さて、どうすれば彼に納得感を持って、具体的な行動につなげられるだろうか？
僕自身の経験を話すのもいいが、彼は「指針が見えない」と言っている。ならば、客観的で包括的なアドバイスが必要だ。
こういう時こそ、最新のAIを頼ってみよう。僕の頭の中にあるベストプラクティスを言語化する助けにもなるし、第三者の視点として彼にも受け入れやすいはずだ。

よし、今回はGeminiに相談してみよう。

### AI (Gemini) への指示

「私がシニアエンジニアとして若手エンジニア（Java/C#初心者、入社1-3年目）にコードレビューの作法を伝えるためのアドバイスを求めています。特に、『動けばいい』から『保守性の高いコード』へのステップアップを目指す彼らに向けたものです。」

「若手エンジニアがコードレビューで指摘されがちな点を改善するための、保守性の高いコードの書き方について、具体的なJavaとC#のコード例（簡潔なもの）を交えて解説してください。以下の観点を含めてください。」

*   **可読性**: 命名規則、コメント、コードフォーマット
*   **変更容易性**: 単一責任の原則 (SRP)、マジックナンバーの排除
*   **テスト容易性**: 依存性の注入 (DI) の考え方、テストしやすい設計
*   **DRY原則**: 重複コードの排除
*   **単一責任の原則 (SRP)**: クラスやメソッドの役割分担

「加えて、コードレビューを受ける側の心構え、指摘をどう活かすかについても助言をお願いします。出力はMarkdown形式でお願いします。」

### AIの回答

> ## コードレビューで学ぶ保守性の高いコードの書き方と心構え
>
> 若手エンジニアの皆さん、コードレビューは皆さんの成長を大きく加速させる貴重な機会です。指摘を恐れる必要はありません。それは「より良いコード」へ導くための道標だと捉えましょう。
>
> ### 保守性の高いコードのための設計原則と実践
>
> **1. 可読性（Readability）**
>
> コードは一度書いたら終わりではなく、何度も読み返され、変更されます。自分以外の誰か（未来の自分も含む）が理解しやすいコードを心がけましょう。
>
> *   **適切な命名**: 変数、メソッド、クラス名などは、その目的や役割が明確にわかるように命名しましょう。
>    *   `int a;` よりも `int userCount;`
>    *   `calc()` よりも `calculateTotalPrice()`
> *   **コメントの活用**: なぜこのコードが必要なのか、複雑なロジックの意図など、コードだけでは伝わりにくい情報を補足します。ただし、コードを読めばわかる内容をコメントにするのは避けましょう。
> *   **コードフォーマット**: 一貫したインデント、空白、改行を適用し、視覚的にコードブロックや論理的なまとまりがわかるようにします。チームのコーディング規約に従いましょう。
>
> **2. 変更容易性（Maintainability / Modifiability）**
>
> ビジネス要件は常に変化します。変更が容易なコードは、将来のコスト削減に直結します。
>
> *   **単一責任の原則 (SRP)**: クラスやメソッドは一つの明確な責任だけを持つように設計します。これにより、ある変更が他の部分に与える影響（副作用）を最小限に抑えられます。
> *   **マジックナンバーの排除**: コード中に直接書かれた意味不明な数値（マジックナンバー）は、定数として定義し、名前を付けましょう。
>    *   `if (status == 1)` よりも `if (status == Status.ACTIVE)`
>
> **3. テスト容易性（Testability）**
>
> バグを早期に発見し、安心して変更を加えるためには、テストしやすいコードが不可欠です。
>
> *   **依存性の注入 (DI) の考え方**: クラスが直接他のクラスのインスタンスを生成するのではなく、コンストラクタやセッターを通じて外部から依存オブジェクトを受け取るように設計します。これにより、テスト時にモックオブジェクトを差し込むことが容易になります。
>
>     ```java
>     // BAD: 依存性がハードコードされている
>     public class UserService {
>         private UserRepository userRepository = new UserRepository(); // 直接生成
>         // ...
>     }
>
>     // GOOD: コンストラクタインジェクション
>     public class UserService {
>         private UserRepository userRepository;
>         public UserService(UserRepository userRepository) { // 外部から注入
>             this.userRepository = userRepository;
>         }
>         // ...
>     }
>     ```
>
> **4. DRY原則 (Don't Repeat Yourself)**
>
> 同じロジックや処理が複数の場所に散らばっていると、変更が必要になった際に全ての箇所を修正しなければならず、バグの温床になります。
>
> *   **共通化**: 重複するコードは関数やメソッド、クラスとして抽出し、共通化しましょう。
>
> **5. 単一責任の原則 (SRP) の深化**
>
> 先述の通りですが、これは特に重要です。例えば、ユーザー情報を扱うクラスが「ユーザーデータの永続化」「ユーザーのバリデーション」「ユーザーへの通知」といった複数の異なる責任を持っている場合、どれか一つに変更があっただけで、他の責任に関わるテストやコードにも影響が出やすくなります。
>
> *   **例**: ユーザー登録処理
>     *   `UserService` (ユーザー登録というビジネスロジック全体を管理)
>     *   `UserRepository` (データベース操作の責任)
>     *   `UserValidator` (入力値検証の責任)
>     *   `NotificationService` (通知処理の責任)
>     *   のように、役割を細分化しましょう。
>
> ### コードレビューを受ける側の心構え
>
> 1.  **感謝の気持ち**: レビューは、忙しい時間を割いてあなたのコードを見てくれている証拠です。まずは感謝の気持ちを伝えましょう。
> 2.  **質問する勇気**: 指摘の意図がわからない場合は、遠慮なく質問しましょう。「なぜこの方が良いのでしょうか？」「具体的にどのような状況で問題になる可能性がありますか？」
> 3.  **素直な姿勢**: 指摘は個人的な攻撃ではありません。コードをより良くするための提案です。まずは受け止める姿勢が大切です。
> 4.  **改善へのコミットメント**: 指摘されたら、真摯に改善に取り組みましょう。そして、改善した点や学んだことを伝えることで、レビュアーとの信頼関係も深まります。
> 5.  **事前セルフレビュー**: レビューを依頼する前に、自分で一度読み返し、今回学んだ原則に照らして「もっと良くできないか」を考えてみましょう。AIを使ってセルフレビューするのも有効です。
>
> コードレビューは、チーム全体のコード品質を高め、エンジニア一人ひとりが成長するための文化です。前向きに取り組んでいきましょう！

AI、いい仕事をしてくれたな！特に心構えの部分は、僕が口頭で伝えようとしていたことを綺麗にまとめてくれている。
ただ、コード例はかなり抽象的で、JavaとC#の最新機能が活かされていない。ここを僕が補足して、より具体的なイメージを持たせてあげよう。

## 2. Java vs C# 実装比較：最新機能で保守性を高める

AIの回答で示された「保守性の高いコード」の原則を、JavaとC#の具体的なコードで見ていこう。特に、最新バージョン（Java 21 / C# 12）で使える便利な機能も交えながら解説するよ。

例えば、「ユーザーのIDと名前を受け取って、ユーザーオブジェクトを生成し、そのユーザーが有効かどうかを判断する」というシンプルな機能で考えてみよう。

### Java 21での実装例

AIが指摘した「可読性」や「単一責任の原則」を意識して、Java 21の機能を活用してみる。

```java
// ユーザー情報を表現するレコード（immutableで簡潔）
// データクラスとして、可読性と不変性を高める
public record User(int id, String name, boolean isActive) {
    // コンストラクタで簡易なバリデーションも可能。不正な状態のオブジェクト生成を防ぐ
    public User {
        if (id <= 0) {
            throw new IllegalArgumentException("User ID must be positive.");
        }
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("User name cannot be empty.");
        }
    }
}

// ユーザーの有効性を判断するサービス（単一責任）
// Userオブジェクトの有効性を判断するロジックのみに責任を持つ
public class UserValidationService {
    /**
     * 指定されたユーザーが処理に有効であるかを判断します。
     * アクティブかつIDが偶数である場合にtrueを返します。
     * @param user チェック対象のユーザー
     * @return ユーザーが有効であればtrue、そうでなければfalse
     */
    public boolean isValidUserForProcessing(User user) {
        // switch式とレコードパターンで簡潔に条件分岐。
        // オブジェクトの構造を分解しつつ、可読性の高い条件記述が可能
        return switch (user) {
            case User(var id, _, true) when id % 2 == 0 -> true; // アクティブでIDが偶数
            case User(_, _, false) -> false; // 非アクティブユーザー
            case null -> false; // Nullableな場合はここでパターンマッチング
            default -> false; // その他のケース
        };
    }

    // Unnamed Patterns and Variables (Java 21) を使用した別の例
    // 不要な変数名を`_`で無視することで、コードの意図を明確にする
    public String getUserStatusMessage(Object userObj) {
        return switch (userObj) {
            case User(_, var name, true) -> name + " is active."; // IDは使用しないので_で無視
            case User(_, var name, false) -> name + " is inactive.";
            case null -> "User object is null."; // nullパターンマッチング
            case default -> "Unknown user object type.";
        };
    }
}

// メインメソッドでの利用例
public class Application {
    public static void main(String[] args) {
        User activeUser = new User(10, "Alice", true);
        User inactiveUser = new User(5, "Bob", false);

        UserValidationService validationService = new UserValidationService();

        System.out.println("Alice is valid for processing: " + validationService.isValidUserForProcessing(activeUser)); // true
        System.out.println("Bob is valid for processing: " + validationService.isValidUserForProcessing(inactiveUser)); // false

        System.out.println(validationService.getUserStatusMessage(activeUser)); // Alice is active.
        System.out.println(validationService.getUserStatusMessage(inactiveUser)); // Bob is inactive.
        System.out.println(validationService.getUserStatusMessage(null)); // User object is null.

        try {
            // 不正なユーザー名でUserオブジェクトを生成しようとすると、コンストラクタで例外が発生
            User anotherInvalid = new User(1, "", true);
        } catch (IllegalArgumentException e) {
            System.err.println("Error creating user: " + e.getMessage()); // User name cannot be empty.
        }
    }
}
```

*   **Java 21のポイント**:
    *   `record` クラスは、データを保持するクラスを非常に簡潔に書くための機能で、不変性（immutable）を保証しやすく、可読性を高めます。コンストラクタで初期バリデーションも可能です。
    *   `switch` 式の強化と**レコードパターン** (`case User(var id, _, true)`) により、オブジェクトの構造を分解しながら条件分岐を簡潔に書けます。
    *   **Unnamed Patterns and Variables** (`_`) で、不要な変数を無視でき、コードの意図を明確にします。
    *   Nullに関するパターンマッチングもできるようになり、より安全なコードが書けます。

### C# 12での実装例

同様の機能をC# 12の最新機能で書いてみよう。

```csharp
// ユーザー情報を表現するレコード型（immutableで簡潔）
// C# 12のPrimary ConstructorsとRecordの組み合わせで、データクラスをよりコンパクトに
public record User(int Id, string Name, bool IsActive)
{
    // Primary Constructorで初期化時にバリデーション。不正な状態のオブジェクト生成を防ぐ
    public User
    {
        if (Id <= 0)
        {
            throw new ArgumentException("User ID must be positive.", nameof(Id));
        }
        if (string.IsNullOrWhiteSpace(Name))
        {
            throw new ArgumentException("User name cannot be empty.", nameof(Name));
        }
    }
}

// ユーザーの有効性を判断するサービス（単一責任）
// Userオブジェクトの有効性を判断するロジックのみに責任を持つ
public class UserValidationService
{
    /// <summary>
    /// 指定されたユーザーが処理に有効であるかを判断します。
    /// アクティブかつIDが偶数である場合にtrueを返します。
    /// </summary>
    /// <param name="user">チェック対象のユーザー</param>
    /// <returns>ユーザーが有効であればtrue、そうでなければfalse</returns>
    // C# 12のパターンマッチング強化とラムダ式（式本体のメンバー）
    public bool IsValidUserForProcessing(User user) => user switch
    {
        // プロパティパターンとwhen句で、オブジェクトのプロパティに基づく複雑な条件分岐を簡潔に記述
        { IsActive: true, Id: var id } when id % 2 == 0 => true, // アクティブでIDが偶数
        { IsActive: false } => false, // 非アクティブユーザー
        null => false, // nullの場合
        _ => false // その他のケース
    };

    // C# 12の新しいコレクション式
    // コレクションの初期化や操作をより簡潔に表現
    public IEnumerable<User> GetActiveUsers(IEnumerable<User> users) =>
        [.. users.Where(u => u.IsActive)]; // LINQとコレクション式を組み合わせる
}

// メインメソッドでの利用例
public class Application
{
    public static void Main(string[] args)
    {
        User activeUser = new User(10, "Alice", true);
        User inactiveUser = new User(5, "Bob", false);

        UserValidationService validationService = new UserValidationService();

        Console.WriteLine($"Alice is valid for processing: {validationService.IsValidUserForProcessing(activeUser)}"); // True
        Console.WriteLine($"Bob is valid for processing: {validationService.IsValidUserForProcessing(inactiveUser)}"); // False

        var users = new List<User> { activeUser, inactiveUser, new User(12, "Charlie", true) };
        var activeUsers = validationService.GetActiveUsers(users);
        Console.WriteLine("Active users: " + string.Join(", ", activeUsers.Select(u => u.Name))); // Active users: Alice, Charlie

        try
        {
            // 不正なユーザー名でUserオブジェクトを生成しようとすると、Primary Constructorで例外が発生
            User anotherInvalid = new User(1, "", true);
        }
        catch (ArgumentException e)
        {
            Console.Error.WriteLine($"Error creating user: {e.Message}"); // User name cannot be empty. (Parameter 'Name')
        }
    }
}
```

*   **C# 12のポイント**:
    *   `record` 型はJavaのレコードと同様に不変なデータ型を簡潔に定義できます。
    *   **Primary Constructors** (`public record User(int Id, string Name, bool IsActive)`) により、レコード型やクラスのコンストラクタがより簡潔に書け、初期化時のバリデーションもスマートに記述できます。
    *   **パターンマッチング**の進化 (`{ IsActive: true, Id: var id } when id % 2 == 0`) により、オブジェクトのプロパティを基にした条件分岐が非常に読みやすく、表現力豊かに書けます。
    *   **コレクション式** (`[.. users.Where(u => u.IsActive)]`) は、コレクションの初期化や結合をより簡潔にします。

### 比較と考察

見ての通り、JavaもC#も、**データとロジックを分離し、不変性を活用し、パターンマッチングを駆使することで、コードの可読性、保守性、変更容易性が大幅に向上する**ように進化しています。

*   **データ表現**:
    *   Javaの `record` とC#の `record` は、どちらも不変なデータオブジェクトを簡潔に定義するのに非常に強力です。
*   **条件分岐とデータ分解**:
    *   Javaの `switch` 式とレコードパターン、C#の拡張されたパターンマッチングは、複雑な条件分岐を非常に読みやすくします。特に、オブジェクトの内部構造に基づいた分岐がスマートに書けるのは大きなメリットです。
*   **初期化とバリデーション**:
    *   JavaのレコードコンストラクタとC#のPrimary Constructorsは、オブジェクト生成時のルールを明確にし、不正な状態のオブジェクトが作られることを防ぐのに役立ちます。
*   **DRY / SRP**:
    *   上記のような機能を活用することで、各クラスやメソッドの責任を明確にし、重複するロジックを排除しやすくなります。

これらの最新機能をただ使うだけでなく、「なぜこの機能が生まれたのか」「この機能を使うと、どんな問題が解決され、どんなメリットがあるのか」を理解することが、真の「保守性の高いコード」への道なんだ。

## 3. 若手への一言：明日から使える「お作法」のアドバイス

さて、AIの知恵と僕の経験、そして具体的なコード例を見てきたけれど、一番大切なのは「明日からどう行動するか」だ。コードレビューを最大限に活用するための「お作法」を伝授しよう。

### 🌸 レビューを「する側」としてのお作法

コードレビューは、相手の成長を促し、チームの品質を高めるためのもの。単なる間違い探しではないんだ。

1.  **「なぜ？」を伝える**:
    *   「ここを直してください」だけでなく、「なぜ、この変更が必要なのか」「このままだと将来的に〇〇な問題が発生する可能性がある」といった背景や意図を具体的に伝えよう。
    *   例：「`if/else`が深くなると可読性が落ち、テストも難しくなります。ポリモーフィズムを活用する方向でリファクタリングを検討できませんか？」
2.  **提案は質問形式で**:
    *   「〇〇してください」と命令するのではなく、「〇〇するのはいかがでしょうか？」「〇〇の観点から考えると、別の書き方も考えられますが、どう思われますか？」と、相手の思考を引き出すように。
3.  **良い点も具体的に褒める**:
    *   「ここ、とても良いですね！特に〇〇の点が素晴らしいです。」と具体的に褒めることで、相手は自信を持ち、次も良いコードを書こうとモチベーションを保てる。
4.  **コードの意図を尊重する**:
    *   完璧なコードは存在しない。レビュアー自身の好みに固執せず、コードの目的や設計思想を理解しようと努めよう。
    *   もし意図が不明なら、直接質問するのが一番だ。
5.  **レビューは対話**:
    *   一方的な指摘ではなく、議論を通じて共に最適な解決策を見つける場と捉えよう。必要であれば、直接会ってホワイトボードで話すのも有効だ。

### 🌻 レビューを「される側」としてのお作法

指摘は成長の糧だ。感情的にならず、前向きに受け止め、次へと活かしていく姿勢が何よりも大切だよ。

1.  **感謝から始める**:
    *   「レビューありがとうございます！」の一言は、円滑なコミュニケーションの第一歩だ。
2.  **質問は明確に、遠慮なく**:
    *   指摘の意図がわからない場合は、「〇〇とご指摘いただきましたが、具体的にどのような状況で問題になるでしょうか？」「AとBのどちらが良いか迷ったのですが、先輩はAが良いとお考えですか？」のように、具体的に質問しよう。
    *   決して「指摘が間違っている」という姿勢ではなく、「理解を深めたい」という姿勢で臨むこと。
3.  **素直に受け止める**:
    *   完璧なコードなんて書けない。指摘は、自分の知識や経験が足りなかった部分を補完してくれるものだ。
    *   「動いていたのに…」という気持ちは一旦脇に置いて、「もっと良い方法があるんだな」と前向きに捉えよう。
4.  **改善へのコミットメントと報告**:
    *   指摘された点を修正したら、「〇〇の件、ご指摘いただき修正しました。AからBに変更することで、Cのようなメリットがあると理解できました。ありがとうございました！」と、理解した内容と共に報告しよう。
    *   これにより、レビュアーはあなたの成長を実感し、より親身になってくれるだろう。
5.  **AIを「最初のレビュアー」にする**:
    *   コードを書き終えたら、レビュー依頼を出す前に一度、自分でAI（Geminiなど）に「このコードの改善点を、可読性、保守性、DRY原則の観点から指摘してください」と依頼してみよう。
    *   AIの指摘を元に自分で修正することで、レビュアーからの指摘を減らせるし、自分の思考力も鍛えられる。これはまさに、僕が今回見せた「シニアの思考プロセス」の一部だ。

## 最後に

コードレビューは、単なるコードのチェック作業ではない。
それは、**チーム全体の技術レベルを向上させ、知識を共有し、お互いを信頼し、より良いプロダクトを共に作り上げていくための、かけがえのないコミュニケーションの場**なんだ。

最初は難しく感じるかもしれない。でも、この「お作法」を意識して、日々の開発に取り組んでいけば、きっと君のエンジニアとしての価値は飛躍的に向上するはずだ。

「動けばいい」から卒業し、「保守性の高い、美しいコード」を書けるエンジニアへ。
僕も、そしてチームのみんなも、君たちの成長を心から応援しているよ。
さあ、明日から早速実践してみてくれ！