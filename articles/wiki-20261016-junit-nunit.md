---
title: "【Wiki】単体テスト（JUnit/NUnit） (Java/C# 実装リファレンス)"
emoji: "🛠️"
type: "tech"
topics: ["java", "csharp", "新人教育", "architecture", "wiki"]
published: true
---

## はじめに

チームの皆さん、こんにちは！リードエンジニアの[あなたの名前]です。

この技術リファレンスは、私たちのプロジェクトにおける単体テストのベストプラクティスを共有し、特に若手エンジニアの皆さんがすぐに実践できるよう、「そのまま実行できる」コード例と詳細な解説を提供することを目的としています。単体テストはソフトウェアの品質を担保し、将来にわたる保守性と拡張性を高めるための最も基本的な、しかし最も重要な活動の一つです。

ここでは、Javaにおける**JUnit 5**とC#における**NUnit 3.x**を対象に、その基本的な使い方から、プロフェッショナルな視点での設計原則、パフォーマンス、そしてバージョンアップに伴う推奨される書き方の変化までを網羅的に解説します。

さあ、堅牢で信頼性の高いコードベースを一緒に構築していきましょう！

## 1. 単体テストの基礎：AAA原則とテストの独立性

### 1.1. 単体テストとは？その目的

単体テスト（Unit Test）は、ソフトウェアの最小単位（通常はメソッドやクラス）が意図した通りに機能するかを検証するテストです。

**主な目的:**

*   **品質保証**: 個々のコンポーネントが正しく動作することを確認し、バグを早期に発見します。
*   **リファクタリングの安全性**: コード変更やリファクタリングを行った際に、既存の機能が壊れていないことを迅速に検証できます。
*   **設計の改善**: テストしやすいコードは、しばしば疎結合で凝集度が高い、優れた設計のコードになります。
*   **ドキュメント**: テストコード自体が、対象コードの期待される振る舞いを具体的に示すドキュメントとしての役割を果たします。

### 1.2. Arrange-Act-Assert (AAA) パターン

単体テストを記述する際の最も一般的で推奨されるパターンが、**Arrange-Act-Assert (AAA)** です。これにより、テストの意図が明確になり、可読性が向上します。

1.  **Arrange (準備)**: テストに必要なオブジェクトの生成、データの準備、モックの設定など、テストの前提条件を整えます。
2.  **Act (実行)**: テスト対象のメソッドや機能を呼び出し、実行します。
3.  **Assert (検証)**: 実行結果が期待通りであるかを検証（アサート）します。

### 1.3. 良い単体テストの特性 (F.I.R.S.T. 原則)

良い単体テストは以下のF.I.R.S.T.原則に従うべきです。

*   **F**ast (高速): テストは高速に実行されるべきです。遅いテストは開発者のフィードバックサイクルを阻害し、テストの実行頻度を低下させます。
*   **I**ndependent (独立): 各テストは他のテストとは独立して実行でき、その結果に影響を与えたり、受けたりしないべきです。テストの実行順序に依存しないようにします。
*   **R**epeatable (再現可能): どのような環境で、何度実行しても同じ結果になるべきです。外部リソース（データベース、ファイルシステム、ネットワーク）への依存は極力避けるか、テストダブルで置き換えます。
*   **S**elf-validating (自己検証可能): テストは実行結果（成功/失敗）を明確に示すべきです。手動での検証は不要です。
*   **T**imely (適時): テストは、テスト対象のコードを書くのと同時、またはその直前に書かれるべきです（TDD: テスト駆動開発）。

### 1.4. テスト対象 (SUT: System Under Test) の特定と独立性

単体テストでは、テスト対象を可能な限り小さな単位に限定します。通常は1つのクラスやメソッドがSUTとなります。

SUTが外部の依存関係（他のクラス、データベース、外部サービスなど）を持つ場合、それらの依存関係を「テストダブル」（モック、スタブなど）に置き換えることで、SUTのテストを独立させ、再現性を高めます。これにより、外部依存の不具合やパフォーマンスの問題がテスト結果に影響するのを防ぎます。

## 2. JUnit 5 による単体テスト (Java)

JavaにおけるデファクトスタンダードのテストフレームワークであるJUnitの最新バージョン、JUnit 5について解説します。

### 2.1. 準備：依存関係の追加

MavenまたはGradleでプロジェクトを構築している場合、`pom.xml` または `build.gradle` に以下の依存関係を追加します。

**Maven (pom.xml)**

```xml
<dependencies>
    <!-- JUnit Jupiter API for writing tests -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-api</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
    </dependency>
    <!-- JUnit Jupiter Engine for running tests -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter-engine</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
    </dependency>
    <!-- JUnit Platform Launcher for discovering and running tests -->
    <dependency>
        <groupId>org.junit.platform</groupId>
        <artifactId>junit-platform-launcher</artifactId>
        <version>1.10.0</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

**Gradle (build.gradle)**

```gradle
dependencies {
    testImplementation 'org.junit.jupiter:junit-jupiter-api:5.10.0'
    testRuntimeOnly 'org.junit.jupiter:junit-jupiter-engine:5.10.0'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher' // IDEやビルドツールがテストを実行するために必要
}

test {
    useJUnitPlatform() // GradleがJUnit 5のテストを実行するように設定
}
```

### 2.2. テスト対象クラス (SUT) の定義

シンプルな四則演算を行う`CalculatorService`クラスをテスト対象とします。

**`src/main/java/com/example/service/CalculatorService.java`**

```java
package com.example.service;

/**
 * シンプルな四則演算サービス。
 */
public class CalculatorService {

    /**
     * 2つの整数を加算します。
     * @param a 1つ目の整数
     * @param b 2つ目の整数
     * @return 加算結果
     */
    public int add(int a, int b) {
        return a + b;
    }

    /**
     * 2つの整数を減算します。
     * @param a 1つ目の整数
     * @param b 2つ目の整数
     * @return 減算結果
     */
    public int subtract(int a, int b) {
        return a - b;
    }

    /**
     * 2つの整数を乗算します。
     * @param a 1つ目の整数
     * @param b 2つ目の整数
     * @return 乗算結果
     */
    public int multiply(int a, int b) {
        return a * b;
    }

    /**
     * 2つの整数を除算します。
     * @param a 割られる数
     * @param b 割る数
     * @return 除算結果
     * @throws IllegalArgumentException 割る数が0の場合
     */
    public double divide(int a, int b) {
        if (b == 0) {
            throw new IllegalArgumentException("Cannot divide by zero");
        }
        return (double) a / b;
    }
}
```

### 2.3. 基本的なテストメソッド

`@Test` アノテーションを付与したメソッドがテストメソッドとして認識されます。
`Assertions` クラスを使って結果を検証します。

**`src/test/java/com/example/service/CalculatorServiceTest.java`**

```java
package com.example.service;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * CalculatorServiceの単体テストクラス。
 */
@DisplayName("CalculatorServiceのテスト") // テストクラスに表示名を設定
class CalculatorServiceTest {

    private CalculatorService calculator; // テスト対象のインスタンス

    /**
     * 各テストメソッドの実行前に初期化処理を行います。
     * AAAパターンのArrangeフェーズの一部です。
     */
    @BeforeEach
    void setUp() {
        // 各テストが独立して実行されるよう、新しいインスタンスを生成
        calculator = new CalculatorService();
    }

    @Test
    @DisplayName("加算が正しく行われること") // テストメソッドに表示名を設定
    void testAdd() {
        // Arrange (準備): setUp()でCalculatorServiceが初期化済み
        int num1 = 5;
        int num2 = 3;

        // Act (実行): 加算メソッドを呼び出す
        int result = calculator.add(num1, num2);

        // Assert (検証): 期待される結果と比較する
        Assertions.assertEquals(8, result, "5 + 3 は 8 であるべきです");
    }

    @Test
    @DisplayName("減算が正しく行われること")
    void testSubtract() {
        // Arrange
        int num1 = 10;
        int num2 = 4;

        // Act
        int result = calculator.subtract(num1, num2);

        // Assert
        Assertions.assertEquals(6, result, "10 - 4 は 6 であるべきです");
    }

    @Test
    @DisplayName("乗算が正しく行われること")
    void testMultiply() {
        // Arrange
        int num1 = 6;
        int num2 = 7;

        // Act
        int result = calculator.multiply(num1, num2);

        // Assert
        Assertions.assertEquals(42, result, "6 * 7 は 42 であるべきです");
    }

    @Test
    @DisplayName("除算が正しく行われること")
    void testDivide() {
        // Arrange
        int num1 = 10;
        int num2 = 2;

        // Act
        double result = calculator.divide(num1, num2);

        // Assert
        Assertions.assertEquals(5.0, result, 0.001, "10 / 2 は 5.0 であるべきです (許容誤差0.001)");
    }

    @Test
    @DisplayName("ゼロ除算でIllegalArgumentExceptionが発生すること")
    void testDivideByZeroThrowsException() {
        // Arrange
        int num1 = 10;
        int num2 = 0;

        // Act & Assert
        // 例外が発生することを検証する際は、assertThrowsを使用します。
        // ラムダ式でテスト対象の処理を囲むことで、例外が適切にキャッチされるかを検証します。
        IllegalArgumentException thrown = Assertions.assertThrows(
            IllegalArgumentException.class,
            () -> calculator.divide(num1, num2),
            "ゼロ除算ではIllegalArgumentExceptionがスローされるべきです"
        );

        // 例外メッセージが期待通りであるかも検証できます。
        Assertions.assertEquals("Cannot divide by zero", thrown.getMessage());
    }
}
```

### 2.4. ライフサイクルメソッド

JUnit 5では、テストの実行ライフサイクルを制御するためのアノテーションが提供されています。

*   `@BeforeEach`: 各テストメソッドの**実行前**に実行されます。`setUp()`のような初期化処理に最適です。
*   `@AfterEach`: 各テストメソッドの**実行後**に実行されます。`tearDown()`のような後処理（リソース解放など）に最適です。
*   `@BeforeAll`: **テストクラス内の全テストメソッドの実行前**に一度だけ実行されます。staticメソッドである必要があります。
*   `@AfterAll`: **テストクラス内の全テストメソッドの実行後**に一度だけ実行されます。staticメソッドである必要があります。

#### プロフェッショナルな視点：インスタンスの生存期間とスレッドセーフ

JUnit 5はデフォルトで、テストクラスのインスタンスをテストメソッドごとに生成します（`TestInstance.Lifecycle.PER_METHOD`）。これにより、各テストメソッドが独立した状態を持ち、テスト間の副作用を防ぎ、並列テスト実行時のスレッドセーフティを保証します。

*   **`@BeforeEach` / `@AfterEach` の活用**: 各テストが独立した状態を保つためには、`@BeforeEach`でSUTや依存オブジェクトを毎回新しく生成するのがベストプラクティスです。上記の`CalculatorServiceTest`のように、`setUp()`で`calculator = new CalculatorService();`とすることで、各テストがクリーンな状態から開始されます。

*   **`@BeforeAll` / `@AfterAll` の活用**: これらはテストクラス全体で一度だけ実行されるため、時間のかかるリソースのセットアップ（例: インメモリデータベースの起動、Webサーバーの起動）や、テストデータの大規模な準備に適しています。
    *   **注意点**: `static`メソッドで実行されるため、共有状態を扱うことになります。**並列テスト実行時に複数のテストがこの共有状態を同時に変更しようとすると、競合状態が発生し、テストが不安定になる可能性があります。** `static`フィールドや`@BeforeAll`/`@AfterAll`を使用する場合は、そのリソースがスレッドセーフであることを確認するか、テストが並列実行されないように設定する必要があります。
    *   **メモリ効率**: 巨大なオブジェクトを毎回生成するのがメモリ効率が悪い場合、`@BeforeAll`で一度だけ生成して`static`フィールドに保持することも考えられますが、前述のスレッドセーフティの問題を解決する必要があります。テストスイート全体のメモリ使用量と、テストの独立性・安定性のトレードオフを考慮してください。

### 2.5. アサーションの種類と推奨される書き方

JUnit 5の`org.junit.jupiter.api.Assertions`クラスには、多様なアサーションメソッドが用意されています。

*   **`assertEquals(expected, actual, [message])`**: 2つの値が等しいことを検証。
*   **`assertTrue(condition, [message])` / `assertFalse(condition, [message])`**: 条件が真/偽であることを検証。
*   **`assertNull(object, [message])` / `assertNotNull(object, [message])`**: オブジェクトがnull/nullではないことを検証。
*   **`assertThrows(expectedType, executable, [message])`**: 指定された例外がスローされることを検証。Java 8のラムダ式を引数に取ります。
*   **`assertDoesNotThrow(executable, [message])`**: 指定された処理が例外をスローしないことを検証。
*   **`assertTimeout(duration, executable, [message])`**: 指定された処理が制限時間内に完了することを検証。
*   **`assertAll(executables...)`**: 複数のアサーションをまとめて実行し、全てのアサーション結果を報告します。最初の失敗で停止せず、全ての失敗を報告するため、テストのデバッグがしやすくなります。

**`assertAll`の使用例**

```java
// CalculatorServiceTest.java 内に追加
import org.junit.jupiter.api.assertAll; // static import することで Assertions.assertAll と書かずに済む

// ...省略...

    @Test
    @DisplayName("複数の基本的な演算が正しく行われること (assertAll)")
    void testMultipleOperations() {
        // Arrange は setUp() で実施済み

        // Act & Assert
        assertAll("複数の計算結果を検証",
            () -> Assertions.assertEquals(8, calculator.add(5, 3), "5 + 3"),
            () -> Assertions.assertEquals(2, calculator.subtract(5, 3), "5 - 3"),
            () -> Assertions.assertEquals(15, calculator.multiply(5, 3), "5 * 3")
        );
    }
```

### 2.6. パラメータ化テスト (`@ParameterizedTest`)

同じテストロジックで異なる複数の入力値を検証したい場合に便利です。テストの重複を減らし、網羅性を高めます。

*   `@ValueSource`: プリミティブ型や`String`の単一引数を指定。
*   `@CsvSource`: CSV形式で複数の引数を指定。
*   `@MethodSource`: テストメソッドと同じクラスまたは別のクラスのstaticメソッドから`Stream`や`Iterable`でデータを提供。

**`CalculatorServiceTest.java` (パラメータ化テストの追加例)**

```java
package com.example.service;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest; // ParameterizedTestをインポート
import org.junit.jupiter.params.provider.CsvSource; // CsvSourceをインポート
import org.junit.jupiter.params.provider.MethodSource; // MethodSourceをインポート
import org.junit.jupiter.params.provider.ValueSource; // ValueSourceをインポート

import java.util.stream.Stream; // Streamをインポート

import static org.junit.jupiter.api.Assertions.assertAll; // static import

// ...省略...

    @ParameterizedTest(name = "加算テスト: {0} + {1} = {2}") // テスト名にパラメータを表示
    @CsvSource({ // CSV形式で複数の入力と期待値を定義
        "1, 2, 3",
        "0, 0, 0",
        "-1, 1, 0",
        "10, -5, 5"
    })
    @DisplayName("パラメータ化テスト: CsvSourceで加算を検証")
    void testAddWithCsvSource(int a, int b, int expected) {
        // Arrange
        // (setUp()でcalculatorは初期化済み)

        // Act
        int result = calculator.add(a, b);

        // Assert
        Assertions.assertEquals(expected, result);
    }

    @ParameterizedTest(name = "除算テスト: {0} / {1} = {2}")
    @MethodSource("divideTestData") // staticメソッドからテストデータを提供
    @DisplayName("パラメータ化テスト: MethodSourceで除算を検証")
    void testDivideWithMethodSource(int numerator, int denominator, double expected) {
        // Arrange
        // (setUp()でcalculatorは初期化済み)

        // Act
        double result = calculator.divide(numerator, denominator);

        // Assert
        Assertions.assertEquals(expected, result, 0.001); // double比較は誤差を許容
    }

    // @MethodSourceで使用するテストデータプロバイダメソッド
    private static Stream<org.junit.jupiter.params.provider.Arguments> divideTestData() {
        return Stream.of(
            org.junit.jupiter.params.provider.Arguments.of(10, 2, 5.0),
            org.junit.jupiter.params.provider.Arguments.of(7, 2, 3.5),
            org.junit.jupiter.params.provider.Arguments.of(0, 5, 0.0),
            org.junit.jupiter.params.provider.Arguments.of(-10, 2, -5.0)
        );
    }

    @ParameterizedTest(name = "負の数を乗算すると正しく結果が出るか: {0} * {1}")
    @ValueSource(ints = {-1, -5, -100}) // 単一のint値を複数指定
    @DisplayName("パラメータ化テスト: ValueSourceで負数の乗算を検証")
    void testMultiplyWithNegativeValue(int value) {
        // Arrange
        int num1 = 2; // 固定値
        // (setUp()でcalculatorは初期化済み)

        // Act
        int result = calculator.multiply(num1, value);

        // Assert
        Assertions.assertEquals(num1 * value, result); // num1 * value は期待値
    }
}
```

### 2.7. バージョン・アップデート情報 (JUnit 4からの変更点)

JUnit 5は、JUnit 4から大きな変更が加えられました。主な変更点は以下の通りです。

*   **モジュール化**: `JUnit Platform`, `JUnit Jupiter`, `JUnit Vintage` の3つのサブプロジェクトで構成され、より柔軟な拡張が可能になりました。
*   **アノテーション**: `org.junit.jupiter.api` パッケージに新しいアノテーションが導入されました。
    *   `@Test`: `org.junit.Test` から `org.junit.jupiter.api.Test` へ。
    *   `@Before`, `@After` -> `@BeforeEach`, `@AfterEach`
    *   `@BeforeClass`, `@AfterClass` -> `@BeforeAll`, `@AfterAll` (静的メソッドである必要があります)
    *   `@Ignore` -> `@Disabled`
    *   `@Rule`, `@ClassRule` -> JUnit 5のExtension Model (`@ExtendWith`) に置き換え。
*   **アサーション**: `org.junit.Assert` から `org.junit.jupiter.api.Assertions` へ。メソッドシグネチャの一部も変更され、Java 8のラムダ式活用が推奨されます。特に、メッセージ引数を`Supplier<String>`として渡すことで、メッセージ生成のコストを失敗時のみに抑えることができます。

    ```java
    // JUnit 4
    // Assert.assertEquals("メッセージ", expected, actual);

    // JUnit 5 (メッセージがStringの場合)
    // Assertions.assertEquals(expected, actual, "メッセージ");

    // JUnit 5 (メッセージがSupplier<String>の場合 - 推奨)
    // Assertions.assertEquals(expected, actual, () -> "詳細なメッセージはテスト失敗時のみ生成される");
    ```

## 3. NUnit 3.x による単体テスト (C#)

C#における代表的なテストフレームワークであるNUnitの最新バージョン、NUnit 3.xについて解説します。

### 3.1. 準備：依存関係の追加

.NET CLIまたはNuGetパッケージマネージャーでプロジェクトを構築している場合、テストプロジェクトの`.csproj`ファイルに以下の依存関係を追加します。

**テストプロジェクトの `.csproj` ファイル**

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework> <!-- 使用しているターゲットフレームワークに合わせて変更 -->
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <!-- NUnitフレームワーク本体 -->
    <PackageReference Include="NUnit" Version="3.14.0" />
    <!-- テストエクスプローラーでNUnitテストを検出・実行するためのアダプター -->
    <PackageReference Include="NUnit3TestAdapter" Version="4.5.0" />
    <!-- .NET SDKにテストサポートを追加 -->
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
    <!-- NUnit専用のアナライザー (任意だが推奨) -->
    <PackageReference Include="NUnit.Analyzers" Version="3.9.0" />
  </ItemGroup>

  <ItemGroup>
    <!-- テスト対象のプロジェクトへの参照を追加 -->
    <!-- WikiApp.csproj は CalculatorService が含まれるプロジェクトを想定 -->
    <ProjectReference Include="..\WikiApp\WikiApp.csproj" />
  </ItemGroup>

</Project>
```

### 3.2. テスト対象クラス (SUT) の定義

Javaの例と同様に、`CalculatorService`クラスをテスト対象とします。

**`WikiApp/Services/CalculatorService.cs`**

```csharp
namespace WikiApp.Services
{
    /**
     * シンプルな四則演算サービス。
     */
    public class CalculatorService
    {
        /// <summary>
        /// 2つの整数を加算します。
        /// </summary>
        /// <param name="a">1つ目の整数</param>
        /// <param name="b">2つ目の整数</param>
        /// <returns>加算結果</returns>
        public int Add(int a, int b)
        {
            return a + b;
        }

        /// <summary>
        /// 2つの整数を減算します。
        /// </summary>
        /// <param name="a">1つ目の整数</param>
        /// <param name="b">2つ目の整数</param>
        /// <returns>減算結果</returns>
        public int Subtract(int a, int b)
        {
            return a - b;
        }

        /// <summary>
        /// 2つの整数を乗算します。
        /// </summary>
        /// <param name="a">1つ目の整数</param>
        /// <param name="b">2つ目の整数</param>
        /// <returns>乗算結果</returns>
        public int Multiply(int a, int b)
        {
            return a * b;
        }

        /// <summary>
        /// 2つの整数を除算します。
        /// </summary>
        /// <param name="a">割られる数</param>
        /// <param name="b">割る数</param>
        /// <returns>除算結果</returns>
        /// <exception cref="ArgumentException">割る数が0の場合</exception>
        public double Divide(int a, int b)
        {
            if (b == 0)
            {
                throw new ArgumentException("Cannot divide by zero");
            }
            return (double)a / b;
        }
    }
}
```

### 3.3. 基本的なテストメソッド

`[Test]` アトリビュートを付与したメソッドがテストメソッドとして認識されます。
`Assert` クラスを使って結果を検証します。

**`WikiApp.Tests/CalculatorServiceTests.cs`**

```csharp
using NUnit.Framework; // NUnitのアトリビュートやAssertクラスを使用するために必要
using WikiApp.Services; // テスト対象のCalculatorServiceを使用するために必要

namespace WikiApp.Tests
{
    [TestFixture] // このクラスがテストを含むことをNUnitに示します
    [Category("Unit")] // テストをカテゴリ別にグループ化できます (任意)
    public class CalculatorServiceTests
    {
        private CalculatorService _calculator; // テスト対象のインスタンス

        /// <summary>
        /// 各テストメソッドの実行前に初期化処理を行います。
        /// AAAパターンのArrangeフェーズの一部です。
        /// </summary>
        [SetUp]
        public void SetUp()
        {
            // 各テストが独立して実行されるよう、新しいインスタンスを生成
            _calculator = new CalculatorService();
        }

        [Test] // このメソッドがテストメソッドであることを示します
        [Description("加算が正しく行われること")] // テストに説明を追加 (任意)
        public void Add_GivenTwoNumbers_ReturnsCorrectSum()
        {
            // Arrange (準備): SetUp()でCalculatorServiceが初期化済み
            int num1 = 5;
            int num2 = 3;

            // Act (実行): 加算メソッドを呼び出す
            int result = _calculator.Add(num1, num2);

            // Assert (検証): 期待される結果と比較する
            Assert.AreEqual(8, result, "5 + 3 は 8 であるべきです");
        }

        [Test]
        [Description("減算が正しく行われること")]
        public void Subtract_GivenTwoNumbers_ReturnsCorrectDifference()
        {
            // Arrange
            int num1 = 10;
            int num2 = 4;

            // Act
            int result = _calculator.Subtract(num1, num2);

            // Assert
            Assert.AreEqual(6, result, "10 - 4 は 6 であるべきです");
        }

        [Test]
        [Description("乗算が正しく行われること")]
        public void Multiply_GivenTwoNumbers_ReturnsCorrectProduct()
        {
            // Arrange
            int num1 = 6;
            int num2 = 7;

            // Act
            int result = _calculator.Multiply(num1, num2);

            // Assert
            Assert.AreEqual(42, result, "6 * 7 は 42 であるべきです");
        }

        [Test]
        [Description("除算が正しく行われること")]
        public void Divide_GivenTwoNumbers_ReturnsCorrectQuotient()
        {
            // Arrange
            int num1 = 10;
            int num2 = 2;

            // Act
            double result = _calculator.Divide(num1, num2);

            // Assert
            Assert.AreEqual(5.0, result, 0.001, "10 / 2 は 5.0 であるべきです (許容誤差0.001)");
        }

        [Test]
        [Description("ゼロ除算でArgumentExceptionが発生すること")]
        public void Divide_ByZero_ThrowsArgumentException()
        {
            // Arrange
            int num1 = 10;
            int num2 = 0;

            // Act & Assert
            // 例外が発生することを検証する際は、Assert.Throwsを使用します。
            // ラムダ式でテスト対象の処理を囲むことで、例外が適切にキャッチされるかを検証します。
            var ex = Assert.Throws<ArgumentException>(() => _calculator.Divide(num1, num2));

            // 例外メッセージが期待通りであるかも検証できます。
            Assert.That(ex.Message, Does.StartWith("Cannot divide by zero"));
        }
    }
}
```

### 3.4. ライフサイクルメソッド

NUnit 3.xでは、テストの実行ライフサイクルを制御するためのアトリビュートが提供されています。

*   `[SetUp]`: 各テストメソッドの**実行前**に実行されます。`SetUp()`のような初期化処理に最適です。
*   `[TearDown]`: 各テストメソッドの**実行後**に実行されます。`TearDown()`のような後処理（リソース解放など）に最適です。
*   `[OneTimeSetUp]`: **テストクラス内の全テストメソッドの実行前**に一度だけ実行されます。
*   `[OneTimeTearDown]`: **テストクラス内の全テストメソッドの実行後**に一度だけ実行されます。

#### プロフェッショナルな視点：インスタンスの生存期間とスレッドセーフ

NUnitもデフォルトで、テストクラスのインスタンスを各テストメソッドの実行ごとに生成します。これにより、各テストメソッドが独立した状態を持ち、テスト間の副作用を防ぎ、並列テスト実行時のスレッドセーフティを保証します。

*   **`[SetUp]` / `[TearDown]` の活用**: 各テストが独立した状態を保つためには、`[SetUp]`でSUTや依存オブジェクトを毎回新しく生成するのがベストプラクティスです。上記の`CalculatorServiceTests`のように、`SetUp()`で`_calculator = new CalculatorService();`とすることで、各テストがクリーンな状態から開始されます。

*   **`[OneTimeSetUp]` / `[OneTimeTearDown]` の活用**: これらはテストクラス全体で一度だけ実行されるため、時間のかかるリソースのセットアップ（例: インメモリデータベースの起動、Webサーバーの起動）や、テストデータの大規模な準備に適しています。
    *   **注意点**: `[OneTimeSetUp]`や`[OneTimeTearDown]`が実行されるメソッドや、それらが操作する静的フィールドは、複数のテストが共有状態を扱うことになります。**並列テスト実行時に競合状態が発生し、テストが不安定になる可能性があります。**共有リソースを使用する場合は、そのリソースがスレッドセーフであることを確認するか、テストが並列実行されないように設定する必要があります。
    *   **メモリ効率**: 巨大なオブジェクトを毎回生成するのがメモリ効率が悪い場合、`[OneTimeSetUp]`で一度だけ生成して静的フィールドに保持することも考えられますが、前述のスレッドセーフティの問題を解決する必要があります。テストスイート全体のメモリ使用量と、テストの独立性・安定性のトレードオフを考慮してください。

### 3.5. アサーションの種類と推奨される書き方

NUnitの`Assert`クラスには多様なアサーションメソッドが用意されていますが、NUnit 3以降では**Constraint Model (`Assert.That`)** の使用が推奨されています。これはより柔軟で読みやすいアサーションを提供します。

*   **従来のAssertメソッド**: `Assert.AreEqual`, `Assert.IsTrue`, `Assert.IsNull`, `Assert.Throws` など。
*   **Constraint Model (`Assert.That`)**: `Assert.That(actual, Is.EqualTo(expected))`, `Assert.That(actual, Is.GreaterThan(other))`, `Assert.That(actual, Does.Contain(substring))`, `Assert.That(actual, Throws.ArgumentException)` など。

**`Assert.That` の使用例**

```csharp
// CalculatorServiceTests.cs 内に追加

// ...省略...

        [Test]
        [Description("複数の基本的な演算が正しく行われること (Constraint Model)")]
        public void MultipleOperations_ReturnCorrectResults_WithConstraintModel()
        {
            // Arrange は SetUp() で実施済み

            // Act & Assert (複数のアサーションをまとめて記述可能)
            // NUnitにはJUnit 5のassertAllのような明確な機能はありませんが、
            // 複数のAssert.Thatを連続して書くことで、それに近い可読性を実現できます。
            Assert.That(_calculator.Add(5, 3), Is.EqualTo(8), "5 + 3");
            Assert.That(_calculator.Subtract(5, 3), Is.EqualTo(2), "5 - 3");
            Assert.That(_calculator.Multiply(5, 3), Is.EqualTo(15), "5 * 3");

            // 例外のアサーションもより記述的に
            Assert.That(() => _calculator.Divide(10, 0), Throws.ArgumentException.With.Message.Contains("Cannot divide by zero"));
        }

        [Test]
        [Description("文字列が特定のプレフィックスで始まること")]
        public void String_Starts_With_Prefix()
        {
            string message = "Hello World";
            Assert.That(message, Does.StartWith("Hello"));
        }
```

### 3.6. パラメータ化テスト (`[TestCase]`, `[TestCaseSource]`)

同じテストロジックで異なる複数の入力値を検証したい場合に便利です。

*   `[TestCase]`: テストメソッドの引数に直接、テストケースの値を指定します。
*   `[TestCaseSource]`: テストメソッドと同じクラスまたは別のクラスのstaticプロパティやメソッドから`IEnumerable`でデータを提供します。

**`CalculatorServiceTests.cs` (パラメータ化テストの追加例)**

```csharp
using NUnit.Framework;
using WikiApp.Services;
using System.Collections.Generic; // IEnumerable<object[]> を使用するために必要

namespace WikiApp.Tests
{
    [TestFixture]
    [Category("Unit")]
    public class CalculatorServiceTests
    {
        private CalculatorService _calculator;

        [SetUp]
        public void SetUp()
        {
            _calculator = new CalculatorService();
        }

        // ...省略... (既存のテストメソッド)

        [TestCase(1, 2, 3)] // 複数のテストケースをTestCaseアトリビュートで直接指定
        [TestCase(0, 0, 0)]
        [TestCase(-1, 1, 0)]
        [TestCase(10, -5, 5)]
        [Description("パラメータ化テスト: TestCaseで加算を検証")]
        public void Add_GivenVariousNumbers_ReturnsCorrectSum(int a, int b, int expected)
        {
            // Arrange (SetUp()で_calculatorは初期化済み)

            // Act
            int result = _calculator.Add(a, b);

            // Assert
            Assert.AreEqual(expected, result);
        }

        [TestCaseSource(nameof(DivideTestData))] // staticプロパティ/メソッドからテストデータを提供
        [Description("パラメータ化テスト: TestCaseSourceで除算を検証")]
        public void Divide_GivenVariousNumbers_ReturnsCorrectQuotient(int numerator, int denominator, double expected)
        {
            // Arrange
            // (SetUp()で_calculatorは初期化済み)

            // Act
            double result = _calculator.Divide(numerator, denominator);

            // Assert
            Assert.AreEqual(expected, result, 0.001); // double比較は誤差を許容
        }

        // [TestCaseSource]で使用するテストデータプロバイダ
        public static IEnumerable<object[]> DivideTestData
        {
            get
            {
                yield return new object[] { 10, 2, 5.0 };
                yield return new object[] { 7, 2, 3.5 };
                yield return new object[] { 0, 5, 0.0 };
                yield return new object[] { -10, 2, -5.0 };
            }
        }
        
        [TestCaseSource(typeof(CalculatorTestData), nameof(CalculatorTestData.MultiplyTestData))]
        [Description("パラメータ化テスト: 外部クラスのTestCaseSourceで乗算を検証")]
        public void Multiply_GivenVariousNumbers_ReturnsCorrectProduct(int a, int b, int expected)
        {
            // Arrange
            // (SetUp()で_calculatorは初期化済み)

            // Act
            int result = _calculator.Multiply(a, b);

            // Assert
            Assert.AreEqual(expected, result);
        }
    }

    // テストデータを提供する外部クラスの例
    public static class CalculatorTestData
    {
        public static IEnumerable<object[]> MultiplyTestData
        {
            get
            {
                yield return new object[] { 2, 3, 6 };
                yield return new object[] { -2, 3, -6 };
                yield return new object[] { 0, 5, 0 };
            }
        }
    }
}
```

### 3.7. 非同期処理のテスト (`async`/`await`)

NUnit 3以降は、`async`/`await`キーワードを使用して非同期メソッドを直接テストできます。

```csharp
using NUnit.Framework;
using System.Threading.Tasks; // Taskを使用するために必要

namespace WikiApp.Tests
{
    public class AsyncService
    {
        public async Task<string> GetDataAsync()
        {
            await Task.Delay(10); // 非同期処理をシミュレート
            return "Async Data";
        }

        public async Task DoSomethingAsync(bool shouldThrow)
        {
            await Task.Delay(10);
            if (shouldThrow)
            {
                throw new InvalidOperationException("Something went wrong asynchronously.");
            }
        }
    }

    [TestFixture]
    public class AsyncServiceTests
    {
        private AsyncService _service;

        [SetUp]
        public void SetUp()
        {
            _service = new AsyncService();
        }

        [Test]
        public async Task GetDataAsync_ReturnsCorrectString()
        {
            // Act
            string result = await _service.GetDataAsync();

            // Assert
            Assert.That(result, Is.EqualTo("Async Data"));
        }

        [Test]
        public void DoSomethingAsync_ThrowsExceptionWhenExpected()
        {
            // Asyncメソッドが例外をスローする場合、Assert.ThrowsAsyncを使用します
            Assert.ThrowsAsync<InvalidOperationException>(async () => await _service.DoSomethingAsync(true));
        }

        [Test]
        public async Task DoSomethingAsync_DoesNotThrowExceptionWhenNotExpected()
        {
            // 例外が発生しないことを確認するには、awaitで呼び出すだけで十分です
            // 例外が発生した場合、テストは自動的に失敗します
            await _service.DoSomethingAsync(false);
            Assert.Pass("例外がスローされませんでした"); // 明示的にパスを示す
        }
    }
}
```

### 3.8. バージョン・アップデート情報 (NUnit 2からの変更点)

NUnit 3はNUnit 2から大幅な変更が加えられました。

*   **Constraint Modelの導入**: `Assert.That`を使ったアサーションが推奨されるようになりました。これにより、より表現力豊かで読みやすいアサーションが可能です。
*   **非同期テストのサポート**: `async`/`await`キーワードを使用した非同期テストがネイティブにサポートされました。
*   **テスト検出と実行の改善**: テストランナーとフレームワークが分離され、より近代的なテスト環境との統合が容易になりました。
*   **アトリビュートの変更**: いくつかのアトリビュートが変更または削除されました。
    *   `[TestFixtureSetUp]` -> `[OneTimeSetUp]`
    *   `[TestFixtureTearDown]` -> `[OneTimeTearDown]`
    *   `[TestFixture]` アトリビュートは、NUnit 3以降では必須ではありませんが、クラス全体がテストフィクスチャであることを明確にするために使用することをお勧めします。
*   **`[ExpectedException]`アトリビュートの削除**: 例外の検証には `Assert.Throws` または `Assert.ThrowsAsync` を使用するようになりました。これは、例外の種類だけでなく、メッセージやプロパティも検証できるため、より強力です。

## 4. プロフェッショナルな単体テストの設計

単体テストをただ書くだけでなく、品質と保守性を高めるためのプロフェッショナルな視点について解説します。

### 4.1. テスト容易性 (Testability) とSOLID原則

テストしやすいコードは、しばしば良い設計のコードと一致します。特に**SOLID原則**は、テスト容易性の高いコードを書くための強力な指針となります。

*   **S (単一責任の原則)**: クラスが単一の責任を持つことで、テスト対象の範囲が明確になり、テストケースをシンプルに保てます。
*   **O (オープン・クローズドの原則)**: 既存のコードを変更せずに拡張できることで、リファクタリング時の影響範囲を限定し、テストの再実施範囲を減らせます。
*   **L (リスコフの置換原則)**: 基底クラスの振る舞いを継承クラスが変更しないことで、テストの振る舞いを予測しやすくします。
*   **I (インターフェース分離の原則)**: クライアントが不要なメソッドに依存しないインターフェースを提供することで、モックやスタブを作成しやすくなります。
*   **D (依存性逆転の原則)**: 具体的な実装ではなく、抽象（インターフェース）に依存することで、テスト時に依存オブジェクトを簡単に差し替え（依存性注入: DI）できるようになり、SUTを孤立させてテストできます。

**依存性注入 (Dependency Injection: DI)** は、テスト容易性を劇的に向上させるための主要なテクニックです。コンストラクタインジェクションを使うことで、SUTの依存関係をテスト時にモックやスタブで置き換えることが容易になります。

```java
// JavaにおけるDIの例
public class OrderService {
    private final ProductRepository productRepository; // 依存対象

    // コンストラクタインジェクション
    public OrderService(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    public void createOrder(String productId, int quantity) {
        // productRepository を利用したロジック
    }
}

// テストコード
public class OrderServiceTest {
    @Test
    void testCreateOrder() {
        // モックフレームワーク (例: Mockito) を使ってProductRepositoryのモックを作成
        ProductRepository mockRepository = Mockito.mock(ProductRepository.class);
        // モックの振る舞いを定義
        Mockito.when(mockRepository.findById("P001")).thenReturn(new Product("P001", 100));

        // モックをコンストラクタ経由で注入
        OrderService orderService = new OrderService(mockRepository);

        orderService.createOrder("P001", 1);

        // モックが期待通りに呼び出されたことを検証
        Mockito.verify(mockRepository).findById("P001");
    }
}
```

### 4.2. テストダブル (Mock, Stub, Spy など)

SUTが外部の依存関係（データベース、ファイルシステム、ネットワークサービス、他の複雑なオブジェクトなど）を持つ場合、それらの依存関係を「テストダブル」に置き換えてテストします。

*   **Dummy Object (ダミー)**: 単に引数を埋めるために使われ、実際には使われないオブジェクト。
*   **Fake Object (フェイク)**: 実際のオブジェクトと似た実装を持つが、本番環境では使えない簡略化された実装（例: インメモリデータベース）。
*   **Stub (スタブ)**: 特定のメソッド呼び出しに対して、事前に決められた値を返すように設定されたオブジェクト。
*   **Spy (スパイ)**: 実際のオブジェクトのメソッドを呼び出すが、その呼び出し情報（引数、呼び出し回数など）を記録するオブジェクト。
*   **Mock (モック)**: 期待される振る舞いを事前に設定し、テスト後にその振る舞いが実際に発生したかを検証するオブジェクト。

モックやスタブを簡単に作成するためのフレームワークとして、Javaでは**Mockito**、C#では**Moq**や**NSubstitute**などがあります。

### 4.3. パフォーマンスとリソース管理

単体テストは高速であるべきですが、時にはパフォーマンスとテストの網羅性・独立性の間でトレードオフが生じます。

*   **メモリ効率**:
    *   **巨大なテストデータの扱い**: 毎回大量のテストデータを生成するのはメモリ的にも時間的にも非効率です。
        *   小規模なテストにはインメモリデータを使用し、必要に応じて`@BeforeAll`/`[OneTimeSetUp]`で一度だけ準備する。
        *   大規模なテストデータが必要な場合は、ファイルからの読み込みや、テストデータ生成ライブラリを検討する。
    *   **オブジェクトの再利用**: `static`フィールドや`@BeforeAll`/`[OneTimeSetUp]`を使って、コストの高いオブジェクトをテストクラス全体で一度だけ生成し、再利用することを検討します。ただし、**スレッドセーフティとテスト間の独立性を犠牲にしない**ように細心の注意を払う必要があります。共有オブジェクトの状態がテストごとに変わると、テストの信頼性が損なわれます。
*   **スレッドセーフ**:
    *   **並列テスト実行**: 現代のテストランナーはテストを並列実行して高速化を図ります。この際、複数のテストが共有リソース（静的フィールド、ファイル、外部DBなど）に同時にアクセスすると、競合状態が発生し、テストが不安定になる（Flaky Test）可能性があります。
    *   **共有状態の排除**: 各テストは完全に独立しているべきです。可能な限り、`@BeforeEach`/`[SetUp]`でSUTやその依存オブジェクトを毎回新しく生成し、テスト固有の状態を保持するようにします。
    *   **テスト対象がマルチスレッドの場合**: テスト対象のコードがマルチスレッドで動作する場合、テストコードもそれを考慮する必要があります。例えば、非同期処理の完了を待つ、複数のスレッドからのアクセスをシミュレートする、などの工夫が必要です。JUnit 5の`assertTimeout`やNUnitの`Assert.ThrowsAsync`などが役立ちます。

### 4.4. テストカバレッジの活用と限界

テストカバレッジは、テストがコードベースのどの程度をカバーしているかを示す指標です。**JaCoCo (Java)** や **dotCover (C#)** などのツールで計測できます。

*   **活用**: テストが不足している箇所（カバレッジが低い箇所）を発見し、重点的にテストを追加するべき場所を特定するのに役立ちます。最低限の品質を保証するための閾値設定にも使えます。
*   **限界**:
    *   **カバレッジ100%は品質100%ではない**: カバレッジが高いからといって、コードが完全に正しく動作することを保証するものではありません。単にコードが実行されたことを示すだけで、その振る舞いが正しく検証されているかは別問題です。
    *   **欠陥の見落とし**: 例えば、誤った結果をアサートしていても、コードが実行されていればカバレッジは計測されます。
    *   **過剰なカバレッジへの執着**: 不要な複雑なテストを書いたり、実装詳細に結合したテストを書いたりして、テストの保守性を低下させる原因になることもあります。

カバレッジはあくまで品質保証の一助となる指標であり、テストの品質（堅牢性、可読性、保守性）を置き換えるものではないことを理解しておくべきです。

## 5. まとめ

このリファレンスでは、単体テストの基本的な概念から、JUnit 5 (Java) および NUnit 3.x (C#) の具体的な実装方法、そしてプロフェッショナルな視点での設計原則や注意点について解説しました。

単体テストは、一度書いたら終わりではありません。コードベースの進化に合わせて、テストもまた進化させる必要があります。

**皆さんに実践してほしいこと:**

*   **新しい機能やバグ修正では、必ず単体テストを記述する。**
*   **既存コードをリファクタリングする際は、その振る舞いを保証するテストがあることを確認する。**
*   **AAAパターンとF.I.R.S.T.原則を意識し、読みやすく保守性の高いテストを書く。**
*   **依存性注入を活用し、テストしやすいコード設計を心がける。**
*   **テスト失敗時は、その原因を深く掘り下げ、テストコードまたはSUTのどちらに問題があるかを特定する。**

単体テストは、開発者の皆さん自身の強力な味方です。恐れることなく、積極的にテストを書き、品質の高いソフトウェア開発を推進していきましょう！

疑問や不明点があれば、いつでも私やチームのベテランメンバーに相談してください。