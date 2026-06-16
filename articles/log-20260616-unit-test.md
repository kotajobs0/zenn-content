---
title: "【Log】AIとの対話で学ぶ：単体テスト設計"
emoji: "🎓"
type: "tech"
topics: ["java", "csharp", "新人教育", "ai", "思考プロセス"]
published: true
---

# 【Log】AIとの対話で学ぶ：単体テスト設計 — 「動けばいい」から「品質と保守性」へ

皆さん、こんにちは。日本を代表する（と自負している）シニアエンジニアの〇〇（あなたの名前を想像してください）です。

新入社員の皆さんも、そろそろ「動くコード」は書けるようになってきた頃でしょうか。素晴らしいことです。しかし、ソフトウェア開発の世界は奥深く、ただ動くだけでは不十分な場面が山ほどあります。特に、システムが大規模になり、長期にわたって運用・保守されることを考えると、「品質」と「保守性」は避けて通れないテーマになります。

今回は、その中でも特に重要でありながら、若手エンジニアがつまずきがちな「単体テスト設計」について、私の思考プロセスを皆さんにお伝えしたいと思います。そして、現代の強力なパートナーであるAI（Gemini）との対話も交えながら、実践的な学びを深めていきましょう。

「動けばいい」から「品質と保守性の高いコード」へ。そのための第一歩が、良い単体テスト設計です。さあ、一緒に旅を始めましょう。

## 1. AIとの対話記録：若手エンジニアの悩みとシニアの思考

### 若手からの相談

ある日、若手の田中君（入社2年目、Java/C#担当）が私の席にやってきました。

👨‍💻 **田中君:** 「先輩、お疲れ様です！最近、単体テストの設計で悩んでまして…。」

👴 **シニア（私）:** 「お、どうした？何か困っていることでもあるのかい？」

👨‍💻 **田中君:** 「はい。一応、動くコードは書けるようになったんですが、テストコードを書くのがどうも億劫で…。正直、カバレッジだけ意識して何となく書いてる部分があります。これって本当に意味あるんですかね？もっと良い設計の仕方ってあるんでしょうか？」

### シニアのあなたの思考

田中君の悩みは、きっと多くの若手エンジニアが一度は抱く疑問だろう。単にカバレッジを上げるだけのテストは、確かに「意味があるのか？」と感じてしまうものだ。しかし、単体テストの本質はそこではない。

私の頭の中では、以下のような思考が巡っていました。

1.  **田中君の悩みへの共感と本質の提示:**
    *   「うん、よくある悩みだ。でも、そこに疑問を持てたのは素晴らしいね。」
    *   「単体テストは、単にコードが動くことを確認するだけじゃないんだ。」
    *   「『カバレッジ』はあくまで指標の一つ。本当に重要なのは、**『何がテストされているのか』**、そして**『どんな品質が保証されているのか』**という点だ。」

2.  **単体テストの真の目的の再定義:**
    *   **品質保証:** 機能が正しく動作することを保証する。
    *   **回帰テスト:** コード変更時に既存機能が壊れていないことを保証する。
    *   **設計のフィードバック:** テストが書きにくいコードは、往々にして設計が悪いコードだ。テスト容易性の高いコードは、それ自体が保守性・拡張性の高いコードである。
    *   **仕様の明確化:** テストケースは、その機能の「振る舞い」を具体的に示すドキュメントにもなる。
    *   **バグの早期発見:** 開発の初期段階でバグを見つけることで、手戻りコストを大幅に削減できる。

3.  **テスト設計の具体的なアプローチの検討:**
    *   「テストケースを洗い出す際には、闇雲に書くのではなく、いくつかの観点から網羅的に考える必要がある。」
    *   「**正常系**（Happy Path）はもちろん重要だが、それだけでは不十分だ。」
    *   「**異常系**（Error Path）や、**境界値**（Boundary Value）の考慮が品質を大きく左右する。」
    *   「また、依存する外部コンポーネント（データベース、外部API、他のサービス）がある場合、それらをどう扱うか？そこで**モック**や**スタブ**の概念が重要になってくる。」

4.  **AIの活用を提案:**
    *   「このあたりは、私から一方的に説明するよりも、AIに一般的な原則を整理してもらうと、体系的に理解しやすいだろう。」
    *   「AIに聞くことで、客観的な視点と、Java/C#両方での具体的なコード例も示してもらえる。それを元に、さらに深く掘り下げていこう。」

### AI (Gemini) への指示

私は田中君にそう伝え、Geminiに以下のようなプロンプトを投げかけました。

```
あなたは経験豊富なソフトウェアエンジニアです。
若手エンジニア向けに、単体テストの設計原則について分かりやすく解説してください。
特に以下の点を具体的に説明してください。

1.  単体テストの重要性と目的。
2.  「テスト容易性の高いコード」とは何か、その特徴と実装のヒント。
3.  具体的なテストケースの洗い出し方（正常系、異常系、境界値分析、同値分割など）。
4.  依存性の注入（DI）とモック/スタブの活用方法。
5.  Java (JUnit, Mockito) と C# (NUnit, Moq) を使用した具体的なコード例を交えてください。
```

### AIの回答

AI（Gemini）は、私の意図を汲み取り、非常に体系的かつ実践的な回答を生成してくれました。

---
## Geminiの回答

### 1. 単体テストの重要性と目的

単体テストは、ソフトウェア開発において最小単位のコンポーネント（メソッド、クラスなど）が意図した通りに動作するかを検証するプロセスです。その目的は多岐にわたります。

*   **バグの早期発見:** 開発サイクルの早い段階で問題を特定し、修正コストを低減します。
*   **品質保証:** 個々のコンポーネントの品質を担保し、システム全体の信頼性を高めます。
*   **リファクタリングの安全性:** コード変更時に既存機能が壊れていないことを保証し、安心してリファクタリングを進められます。
*   **設計の改善:** テストが書きにくいコードは、しばしば設計に問題があることを示唆します。テスト容易性を追求することで、より良い設計につながります。
*   **仕様の明確化:** テストコードは、そのコンポーネントの「あるべき振る舞い」を示す具体的なドキュメントとしても機能します。

### 2. 「テスト容易性の高いコード」とは何か

テスト容易性の高いコードとは、外部からの影響を最小限に抑え、独立してテストしやすいコードのことです。主な特徴と実装のヒントは以下の通りです。

*   **単一責任の原則 (SRP):** 1つのクラスやメソッドが1つの責任だけを持つように設計します。これにより、テスト対象の範囲が明確になり、テストケースがシンプルになります。
*   **依存性の注入 (DI):** クラスが必要とする依存オブジェクトを、new演算子で直接生成するのではなく、コンストラクタやセッター、メソッドの引数を通じて外部から渡すようにします。これにより、テスト時に依存オブジェクトをモックやスタブに置き換えることが容易になります。
*   **副作用の排除:** 可能であれば、メソッドが外部の状態を変更せず、引数に基づいて常に同じ結果を返す「純粋関数」として設計します。
*   **具象クラスへの依存を避ける:** インターフェースや抽象クラスに依存することで、具体的な実装をテスト時に置き換える柔軟性が生まれます。

### 3. 具体的なテストケースの洗い出し方

テストケースを網羅的に設計するためには、以下の手法が有効です。

*   **正常系 (Happy Path):** 最も一般的な、期待通りの入力と出力のケースです。
*   **異常系 (Error Path / Unhappy Path):**
    *   **無効な入力:** null, 空文字, 負の数, 範囲外の値など。
    *   **予期せぬ状態:** 依存するサービスがエラーを返す、ファイルが見つからない、ネットワークが切断されるなど。
    *   **特定の例外発生:** 意図的に例外をスローする状況をテストします。
*   **境界値分析 (Boundary Value Analysis):** 入力値の範囲の「境界」とそのすぐ外側の値をテストします。
    *   例: 0, 1, 最大値-1, 最大値, 最大値+1, 最小値, 最小値+1 など。
*   **同値分割 (Equivalence Partitioning):** 入力データをいくつかの「同値クラス」（同じ振る舞いをする入力のグループ）に分割し、それぞれのクラスから代表的な値を1つ選んでテストします。
    *   例: 「正の整数」「負の整数」「0」のように分割。
*   **特殊なケース:**
    *   リストが空の場合、1つの要素の場合、多数の要素の場合。
    *   文字列が特定のパターンと一致する場合、一致しない場合。
    *   並列処理における競合状態など。

### 4. 依存性の注入（DI）とモック/スタブの活用方法

実際のアプリケーションでは、多くのクラスが他のクラスや外部システムに依存しています。単体テストでは、テスト対象のコンポーネントのみを独立してテストしたい。このとき、依存オブジェクトをテスト用に置き換えるためにDIとモック/スタブを活用します。

*   **依存性の注入 (DI):** テスト対象のクラスのコンストラクタ、セッター、またはメソッドの引数を通じて、依存オブジェクトを渡す設計パターンです。これにより、テスト時には本物の依存オブジェクトの代わりに、ダミーオブジェクトを注入できます。
*   **モック (Mock):** 依存オブジェクトの「振る舞い」を模倣し、テスト対象のコンポーネントが正しく依存オブジェクトと対話したか（特定のメソッドが呼ばれたか、引数は適切だったかなど）を検証するために使用します。状態の変化ではなく、相互作用の検証に重点を置きます。
*   **スタブ (Stub):** 依存オブジェクトからの「応答」をシミュレートするために使用します。特定のメソッドが呼ばれた際に、事前に定義した値を返すように設定します。状態の変更ではなく、特定の戻り値を返すことを目的とします。

**コード例 (DIとモックの概念)**

Java/C#では、DIコンテナ（Spring, .NET Core DI）を使用することが多いですが、単体テストでは手動でDIを行うか、モックライブラリの機能で実現します。

#### Java (JUnit 5 + Mockito)

```java
// テスト対象のインターフェース
interface UserRepository {
    User findById(int id);
    void save(User user);
}

// テスト対象のサービス
class UserService {
    private final UserRepository userRepository;

    // コンストラクタインジェクション
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User getUserInfo(int userId) {
        User user = userRepository.findById(userId);
        if (user == null) {
            throw new IllegalArgumentException("User not found.");
        }
        // ここでさらにユーザー情報を加工するロジックがあるとして
        return user;
    }

    public void registerUser(User user) {
        // 例: ユーザー名重複チェックなど
        userRepository.save(user);
    }
}

// Userクラス（データクラス）
class User {
    private int id;
    private String name;
    // ... getter, setter, constructor
    public User(int id, String name) { this.id = id; this.name = name; }
    public int getId() { return id; }
    public String getName() { return name; }
}


// 単体テストコード
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito; // Mockitoのインポート
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*; // when, verifyなどをインポート

class UserServiceTest {

    private UserService userService;
    private UserRepository userRepositoryMock; // モックオブジェクト

    @BeforeEach
    void setUp() {
        // UserRepositoryのモックを作成
        userRepositoryMock = Mockito.mock(UserRepository.class);
        // モックを注入してUserServiceのインスタンスを生成
        userService = new UserService(userRepositoryMock);
    }

    @Test
    @DisplayName("存在するユーザーIDでユーザー情報を取得できること")
    void testGetUserInfo_ExistingUser() {
        // モックの振る舞いを定義（スタブ的な使い方）
        User expectedUser = new User(1, "TestUser");
        when(userRepositoryMock.findById(1)).thenReturn(expectedUser);

        // テスト対象メソッドの実行
        User actualUser = userService.getUserInfo(1);

        // 結果の検証
        assertNotNull(actualUser);
        assertEquals(expectedUser.getId(), actualUser.getId());
        assertEquals(expectedUser.getName(), actualUser.getName());

        // モックへの呼び出し検証（モック的な使い方）
        verify(userRepositoryMock, times(1)).findById(1);
    }

    @Test
    @DisplayName("存在しないユーザーIDでIllegalArgumentExceptionが発生すること")
    void testGetUserInfo_NonExistingUser() {
        // モックの振る舞いを定義
        when(userRepositoryMock.findById(99)).thenReturn(null);

        // 例外が発生することを確認
        assertThrows(IllegalArgumentException.class, () -> userService.getUserInfo(99));

        // モックへの呼び出し検証
        verify(userRepositoryMock, times(1)).findById(99);
    }

    @Test
    @DisplayName("新しいユーザーが正しく登録されること")
    void testRegisterUser() {
        User newUser = new User(2, "NewUser");

        // saveメソッドは何も返さないので、doNothing()で振る舞いを定義
        // あるいは、voidメソッドの場合はwhen...thenRerturnは使えず、doNothing()やdoThrow()を使う
        doNothing().when(userRepositoryMock).save(newUser);

        userService.registerUser(newUser);

        // saveメソッドがnewUser引数で1回呼び出されたことを検証
        verify(userRepositoryMock, times(1)).save(newUser);
    }
}
```

#### C# (NUnit + Moq)

```csharp
// テスト対象のインターフェース
public interface IUserRepository
{
    User FindById(int id);
    void Save(User user);
}

// テスト対象のサービス
public class UserService
{
    private readonly IUserRepository _userRepository;

    // コンストラクタインジェクション (C# 12ではPrimary Constructorも利用可能)
    public UserService(IUserRepository userRepository)
    {
        _userRepository = userRepository;
    }

    public User GetUserInfo(int userId)
    {
        User? user = _userRepository.FindById(userId);
        if (user == null)
        {
            throw new ArgumentException("User not found.");
        }
        // ここでさらにユーザー情報を加工するロジックがあるとして
        return user;
    }

    public void RegisterUser(User user)
    {
        // 例: ユーザー名重複チェックなど
        _userRepository.Save(user);
    }
}

// Userクラス（データクラス）
public class User
{
    public int Id { get; init; } // C# 9.0 の init-only setter
    public string Name { get; init; }
    public User(int id, string name) { Id = id; Name = name; }
}


// 単体テストコード
using NUnit.Framework;
using Moq; // Moqのインポート
using System;

namespace MyProject.Services.Tests;

[TestFixture]
public class UserServiceTests
{
    private UserService _userService;
    private Mock<IUserRepository> _userRepositoryMock; // Moqのモックオブジェクト

    [SetUp]
    public void Setup()
    {
        // UserRepositoryのモックを作成
        _userRepositoryMock = new Mock<IUserRepository>();
        // モックを注入してUserServiceのインスタンスを生成
        _userService = new UserService(_userRepositoryMock.Object);
    }

    [Test]
    public void GetUserInfo_ExistingUser_ShouldReturnUser()
    {
        // モックの振る舞いを定義（スタブ的な使い方）
        var expectedUser = new User(1, "TestUser");
        _userRepositoryMock.Setup(repo => repo.FindById(1)).Returns(expectedUser);

        // テスト対象メソッドの実行
        User actualUser = _userService.GetUserInfo(1);

        // 結果の検証
        Assert.That(actualUser, Is.Not.Null);
        Assert.That(actualUser.Id, Is.EqualTo(expectedUser.Id));
        Assert.That(actualUser.Name, Is.EqualTo(expectedUser.Name));

        // モックへの呼び出し検証（モック的な使い方）
        _userRepositoryMock.Verify(repo => repo.FindById(1), Times.Once());
    }

    [Test]
    public void GetUserInfo_NonExistingUser_ShouldThrowArgumentException()
    {
        // モックの振る舞いを定義
        _userRepositoryMock.Setup(repo => repo.FindById(99)).Returns((User)null);

        // 例外が発生することを確認
        Assert.Throws<ArgumentException>(() => _userService.GetUserInfo(99));

        // モックへの呼び出し検証
        _userRepositoryMock.Verify(repo => repo.FindById(99), Times.Once());
    }

    [Test]
    public void RegisterUser_NewUser_ShouldCallSave()
    {
        var newUser = new User(2, "NewUser");

        // saveメソッドは何も返さないので、Returns()は不要。
        // Setup()だけでよい。
        _userRepositoryMock.Setup(repo => repo.Save(newUser));

        _userService.RegisterUser(newUser);

        // SaveメソッドがnewUser引数で1回呼び出されたことを検証
        _userRepositoryMock.Verify(repo => repo.Save(newUser), Times.Once());
    }
}
```

---

## 2. Java vs C# 実装比較：具体的なテストコードから学ぶ

AIの回答で単体テストの原則とモックの概念は理解できましたね。それでは、実際のコードでJavaとC#それぞれの書き方を比較しながら、さらに実践的な理解を深めましょう。

AIの例は`UserService`でしたが、もう少しシンプルな`CalculatorService`を使って、テストケースの洗い出し方を具体的に見てみましょう。

### テスト対象のクラス: `CalculatorService`

加算、減算、除算の機能を持つシンプルな計算機サービスです。

#### Java (Java 21)

```java
// src/main/java/com/example/service/CalculatorService.java
package com.example.service;

public class CalculatorService {
    public int add(int a, int b) {
        return a + b;
    }

    public int subtract(int a, int b) {
        return a - b;
    }

    public double divide(int a, int b) {
        if (b == 0) {
            // 異常系: 0での除算はエラー
            throw new IllegalArgumentException("Cannot divide by zero.");
        }
        return (double) a / b;
    }
}
```

#### C# (C# 12)

```csharp
// src/Services/CalculatorService.cs
namespace MyCompany.Services;

public class CalculatorService
{
    public int Add(int a, int b) => a + b;

    public int Subtract(int a, int b) => a - b;

    public double Divide(int a, int b)
    {
        if (b == 0)
        {
            // 異常系: 0での除算はエラー
            throw new ArgumentException("Cannot divide by zero.");
        }
        return (double)a / b;
    }
}
```

### 単体テストコードの実装と比較

それぞれの言語で、AIが説明してくれた「正常系」「異常系」「境界値」の考え方を適用してテストコードを書いてみます。

#### Java (JUnit 5)

```java
// src/test/java/com/example/service/CalculatorServiceTest.java
package com.example.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested; // Nestedテスト用のimport
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest; // パラメータライズドテスト用のimport
import org.junit.jupiter.params.provider.CsvSource; // パラメータライズドテスト用のプロバイダ
import static org.junit.jupiter.api.Assertions.*; // static importでassertEqualsなどを直接利用

class CalculatorServiceTest {

    private CalculatorService calculatorService;

    @BeforeEach // 各テストメソッド実行前に毎回呼ばれる
    void setUp() {
        calculatorService = new CalculatorService();
    }

    @Nested // ネストされたクラスでテストをグループ化
    @DisplayName("加算機能のテスト")
    class AddTests {
        @ParameterizedTest(name = "add({0}, {1}) => {2}") // パラメータライズドテスト
        @CsvSource({
            "2, 3, 5",      // 正常系: 正の数同士
            "-2, 3, 1",     // 正常系: 負の数と正の数
            "0, 0, 0",      // 境界値: ゼロ同士
            "Integer.MAX_VALUE, 1, " + (Integer.MAX_VALUE + 1L), // 境界値: 最大値 (オーバーフローはここでは考慮しない)
            "Integer.MIN_VALUE, -1, " + (Integer.MIN_VALUE - 1L) // 境界値: 最小値 (アンダーフローはここでは考慮しない)
        })
        void testAdd(int a, int b, long expected) { // longで受け取ることで、オーバーフローの計算結果も検証可能
            // Java 21の機能というよりはJUnit 5の機能だが、現代的なテストコードとして紹介
            assertEquals(expected, calculatorService.add(a, b));
        }
    }

    @Nested
    @DisplayName("減算機能のテスト")
    class SubtractTests {
        @Test
        @DisplayName("正常に減算が実行されること")
        void testSubtract() {
            assertEquals(1, calculatorService.subtract(3, 2));    // 正常系
            assertEquals(5, calculatorService.subtract(2, -3));   // 正常系: 負の数との減算
            assertEquals(0, calculatorService.subtract(0, 0));    // 境界値: ゼロ同士
            assertEquals(Integer.MIN_VALUE + 1, calculatorService.subtract(Integer.MIN_VALUE, -1)); // 境界値
        }
    }

    @Nested
    @DisplayName("除算機能のテスト")
    class DivideTests {
        @Test
        @DisplayName("正常に除算が実行されること")
        void testDivide() {
            assertEquals(2.5, calculatorService.divide(5, 2), 0.0001); // 正常系: 浮動小数点数の比較には許容誤差を指定
            assertEquals(-2.0, calculatorService.divide(-4, 2), 0.0001); // 正常系: 負の数
            assertEquals(0.0, calculatorService.divide(0, 5), 0.0001);   // 境界値: ゼロを非ゼロで割る
        }

        @Test
        @DisplayName("ゼロ除算でIllegalArgumentExceptionが発生すること")
        void testDivideByZeroThrowsException() {
            // 異常系: ゼロ除算
            assertThrows(IllegalArgumentException.class.getName(), // 例外クラス名で検証 (またはクラス型でも可)
                         () -> calculatorService.divide(10, 0));
        }
    }
}
```

#### C# (NUnit 3, C# 12の機能を取り入れつつ)

```csharp
// tests/Services/CalculatorServiceTests.cs
using NUnit.Framework;
using System;
using System.Linq; // C#のLINQや拡張メソッドの利用

namespace MyCompany.Services.Tests;

[TestFixture] // NUnitでテストクラスを示すアトリビュート
public class CalculatorServiceTests
{
    private CalculatorService _calculatorService;

    [SetUp] // 各テストメソッド実行前に毎回呼ばれる
    public void Setup()
    {
        _calculatorService = new CalculatorService();
    }

    // C#ではNestedテスト用のNUnit属性はないが、内部クラスで組織化することは可能 (ただしTestFixtureが付かない)
    // NUnit 3.xではTestCase属性やValueSource属性でパラメータライズドテストを記述

    [TestCase(2, 3, 5)]      // 正常系: 正の数同士
    [TestCase(-2, 3, 1)]     // 正常系: 負の数と正の数
    [TestCase(0, 0, 0)]      // 境界値: ゼロ同士
    [TestCase(int.MaxValue, 1, (long)int.MaxValue + 1)] // 境界値: 最大値 (オーバーフローも検証)
    [TestCase(int.MinValue, -1, (long)int.MinValue - 1)] // 境界値: 最小値 (アンダーフローも検証)
    public void Add_ShouldReturnCorrectSum(int a, int b, long expected) // C#ではlongで受け取ることで、オーバーフローの計算結果も検証可能
    {
        // C# 12の機能としては、Primary Constructorを使うことでDIを簡潔に書けるが、
        // 今回のCalculatorServiceは依存性がないため、直接インスタンス化。
        // Assert.That() はNUnitの推奨する書き方
        Assert.That(_calculatorService.Add(a, b), Is.EqualTo(expected));
    }

    [Test]
    public void Subtract_ShouldReturnCorrectDifference()
    {
        Assert.That(_calculatorService.Subtract(3, 2), Is.EqualTo(1));
        Assert.That(_calculatorService.Subtract(2, -3), Is.EqualTo(5));
        Assert.That(_calculatorService.Subtract(0, 0), Is.EqualTo(0));
        Assert.That(_calculatorService.Subtract(int.MinValue, -1), Is.EqualTo(int.MinValue + 1));
    }

    [Test]
    public void Divide_ShouldReturnCorrectQuotient()
    {
        Assert.That(_calculatorService.Divide(5, 2), Is.EqualTo(2.5).Within(0.0001)); // 正常系: 浮動小数点数の比較
        Assert.That(_calculatorService.Divide(-4, 2), Is.EqualTo(-2.0).Within(0.0001));
        Assert.That(_calculatorService.Divide(0, 5), Is.EqualTo(0.0).Within(0.0001));
    }

    [Test]
    public void Divide_ByZero_ShouldThrowArgumentException()
    {
        // 異常系: ゼロ除算
        Assert.Throws<ArgumentException>(() => _calculatorService.Divide(10, 0));
    }

    // C# 12の機能として、例えば以下のような簡潔な記述も可能だが、
    // 単体テスト自体には直接関係ないため参考程度。
    // record struct (C# 10) などもデータクラスとして活用可能。
    /*
    public record CalculationInput(int A, int B); // C# 10 record struct
    [Test]
    public void Add_WithRecordStruct_ShouldReturnCorrectSum()
    {
        var input = new CalculationInput(2, 3);
        Assert.That(_calculatorService.Add(input.A, input.B), Is.EqualTo(5));
    }
    */
}
```

### 比較とポイント

*   **テストフレームワーク:**
    *   **Java:** JUnit 5 (最新のテストフレームワーク。`@DisplayName`, `@Nested`, `@ParameterizedTest`など機能が豊富)
    *   **C#:** NUnit 3 (広く使われているテストフレームワーク。`[TestFixture]`, `[Test]`, `[TestCase]`などが一般的)
*   **アサート:**
    *   **Java:** `Assertions.assertEquals()`など、シンプルで直接的なAPI。JUnit 5からはラムダ式を使った例外テスト`assertThrows()`も非常に読みやすい。
    *   **C#:** `Assert.That(actual, Is.EqualTo(expected))`という形式がNUnitの推奨。より表現力豊かで、複数の条件をチェーンで記述できる（例：`Is.EqualTo(2.5).Within(0.0001)`）。`Assert.Throws<T>()`も同様に強力。
*   **パラメータライズドテスト:**
    *   **Java:** `@ParameterizedTest`と`@CsvSource`などを使って、複数のテストケースを1つのメソッドで簡潔に記述できる。
    *   **C#:** `[TestCase]`アトリビュートで同様のことが可能。
*   **浮動小数点数の比較:**
    *   両言語とも、浮動小数点数の比較には許容誤差（delta, within）を指定することが重要です。これは計算機の特性上、誤差が生じる可能性があるためです。
*   **最新機能の活用:**
    *   今回の例ではDIがないため、Java 21やC# 12の言語機能が直接テストコードに大きく影響する部分は少ないですが、例えば**Javaのレコードクラス**はテスト用のDTOとして、**C#のPrimary Constructor**はDIを用いたクラスの記述をより簡潔にし、結果としてテストしやすいコードにつながります。
    *   特にDIが絡む場合、C#ではPrimary Constructorで依存性を宣言し、Moqでそれをモック化する、といった連携が非常にスムーズです。

この比較を通して、言語やフレームワークの違いはあれど、**「正常系」「異常系」「境界値」を網羅的に考える**というテスト設計の根本的な考え方は共通していることが分かったかと思います。そして、それが結果的に高品質で保守性の高いコードを生み出す源泉となるのです。

## 3. 若手への一言：明日から使える「お作法」のアドバイス

田中君、そして若手エンジニアの皆さん。AIとの対話と具体的なコード比較を通して、単体テスト設計の奥深さを少しは感じてもらえたでしょうか？

「動けばいい」段階を卒業し、「品質と保守性」を意識するようになった君たちは、もう一段上のエンジニアへと成長する準備ができています。最後に、明日からすぐにでも実践できる「お作法」として、私からのアドバイスを贈ります。

1.  **テストコードは「未来の自分へのラブレター」だと思って書くべし！**
    *   未来の自分や、チームの仲間がそのコードを読んだとき、「あぁ、このコードはこういう振る舞いをするんだな」と一目で理解できるようなテストコードを目指しましょう。良いテストコードは、最高のドキュメントになります。

2.  **まず「テストを書くこと」に慣れるべし！**
    *   最初から完璧なテスト設計は難しいです。まずは「この機能にはどんなテストケースが必要か？」を考え、簡単なものからで良いのでテストを書いてみてください。少しずつ経験を積むことで、テスト設計の勘所が養われていきます。

3.  **TDD (テスト駆動開発) を「小さな機能」で試すべし！**
    *   全ての開発でTDDを導入するのはハードルが高いかもしれません。しかし、例えば「新しいバリデーションロジックを追加する」「シンプルな計算ロジックを実装する」といった小さな機能で、「まずテストを書く」習慣を身につけてみてください。コードを書く前にテストを書くことで、設計への意識が格段に高まります。

4.  **依存性の注入（DI）とモック/スタブの活用を躊躇しないべし！**
    *   AIの回答とコード例で見たように、DIはテスト容易性を高めるための強力な設計パターンです。最初は難しく感じるかもしれませんが、積極的に取り入れてみてください。そして、外部依存をモックで切り離すことで、本当にテストしたい部分だけを純粋に検証できるようになります。

5.  **テストコードも本番コードと同じくらい大切にレビューするべし！**
    *   テストコードは本番コードの品質を保証するものです。そのテストコード自体の品質が低ければ、保証の信頼性も落ちます。コードレビューの際には、本番コードだけでなく、テストコードの可読性、網羅性、設計の良さも積極的に議論しましょう。

### 最後に

単体テストは、単なる作業ではありません。それは、私たちが作り出すソフトウェアの品質を高め、未来の保守性を確保し、結果として開発チーム全体の生産性を向上させるための「投資」です。

皆さんの書いたコードが、長く、多くの人に愛されるシステムの一部となることを願っています。
困ったときは、またいつでも相談に来てください。私も、AIという強力な相棒と共に、常に学び続けています。

---
この記事が、皆さんのエンジニアとしての成長の一助となれば幸いです。