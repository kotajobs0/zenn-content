---
title: "【Log】AIとの対話で学ぶ：コレクション操作（Stream/LINQ）"
emoji: "🎓"
type: "tech"
topics: ["java", "csharp", "新人教育", "ai", "思考プロセス"]
published: true
---

## はじめに：若手エンジニアよ、forループから抜け出そう！

新人の皆さん、こんにちは！
「日本のシニアエンジニア代表」として、皆さんの成長を心から応援しています。
突然ですが、皆さん、日々の開発でリストや配列といった「コレクション」を操作する際、ついつい `for` ループや `foreach` ループを多用していませんか？

「え、ダメなんですか！？」

いえいえ、ダメじゃないんです。もちろん動きます。でもね、先輩たちのコードを見ると、`stream()` や `LINQ` なんて見慣れないものがズラッと並んでいて、「なんか難しそう…」と感じているかもしれませんね。

「動けばいい」フェーズを卒業し、一歩先の「保守性の高い、読みやすいコード」を書くための思考プロセスを、今回は **コレクション操作（Stream/LINQ）** をテーマに、AIとの対話形式で一緒に学んでいきましょう。

## 1. AIとの対話記録：若手の悩みからシニアの思考、そしてAIへ

今回は、若手エンジニアからこんな相談を受けました。

---
### **若手からの相談**

「シニアさん、いつもありがとうございます！
最近、コレクション操作で悩んでいます。なんかいつも`for`ループで書いてしまうんですよね… `Stream`とか`LINQ`とか、正直まだピンと来なくて。でも先輩たちのコードを見ると、みんな使ってるし、どう使いこなせばいいんでしょう？」

---
### **シニアエンジニアの思考プロセス**

なるほど、うんうん、よくわかる悩みだ。新人の頃は皆、同じ道を辿るものだよ。`for`ループで書けるからこそ、その先のメリットを感じにくいのは当然だね。

`Stream`や`LINQ`がなぜ推奨されるのか。それは一言で言えば **「コードの意図が明確になるから」** に尽きる。
`for`ループは「どう処理するか」という手続きを細かく記述する。対して`Stream`や`LINQ`は「何をしたいか」という目的や意図を宣言的に記述できるんだ。

例えば、「30歳以上の男性を抽出して、その名前のリストを作る」という処理があったとする。
`for`ループだと、
1. 新しい空のリストを作る
2. 元のリストを一つずつ見ていく
3. 条件（30歳以上 AND 男性）に合うかチェックする
4. 合ったら、その人の名前を新しいリストに追加する
…という**手順**を追うことになる。

一方、`Stream`や`LINQ`だと、
1. フィルターをかける（30歳以上）
2. さらにフィルターをかける（男性）
3. 名前だけを抽出する
4. 結果をリストにまとめる
…という**処理の塊**として表現できる。後者の方が、読み手は「ああ、このリストから、こういう条件で絞り込んで、名前だけ欲しいんだな」と瞬時に理解できるはずだ。

よし、この具体的な例をAIに投げて、比較コードを出力してもらおう。
若手には、この違いをまずは目で見て、感じてもらうのが一番だ。

---
### **AI(Gemini)への指示**

「JavaとC#の両方で、`List<Person>`から『30歳以上の男性のみ』を抽出し、その名前を新しいリストとして返す処理を考えてください。

まず、伝統的な`for`ループ（C#では`foreach`ループ）での実装例を挙げ、次にJava Stream APIとC# LINQを使った実装例を比較してください。

それぞれの実装について、コードの意図がより明確になる点、簡潔性、保守性の観点からコメントを加えてください。
`Person`クラスの定義もお願いします。
出力はMarkdownのコードブロックでお願いします。」

---
### **AI(Gemini)の回答**

```java
// Personクラス (Java)
class Person {
    private String name;
    private int age;
    private String gender; // "Male" or "Female"

    public Person(String name, int age, String gender) {
        this.name = name;
        this.age = age;
        this.gender = gender;
    }

    public String getName() { return name; }
    public int getAge() { return age; }
    public String getGender() { return gender; }

    @Override
    public String toString() {
        return "Person{" +
               "name='" + name + '\'' +
               ", age=" + age +
               ", gender='" + gender + '\'' +
               '}';
    }
}

// データ準備 (Java)
List<Person> people = Arrays.asList(
    new Person("Alice", 25, "Female"),
    new Person("Bob", 30, "Male"),
    new Person("Charlie", 35, "Male"),
    new Person("Diana", 28, "Female"),
    new Person("Eve", 40, "Female"),
    new Person("Frank", 45, "Male")
);

// --- 伝統的なforループ (Java) ---
List<String> namesOfAdultMalesForLoop = new ArrayList<>();
for (Person person : people) {
    if (person.getAge() >= 30 && person.getGender().equals("Male")) {
        namesOfAdultMalesForLoop.add(person.getName());
    }
}
System.out.println("For-loop (Java): " + namesOfAdultMalesForLoop); // [Bob, Charlie, Frank]

// --- Stream API (Java) ---
List<String> namesOfAdultMalesStream = people.stream()
    .filter(person -> person.getAge() >= 30)
    .filter(person -> person.getGender().equals("Male"))
    .map(Person::getName)
    .collect(Collectors.toList());
System.out.println("Stream API (Java): " + namesOfAdultMalesStream); // [Bob, Charlie, Frank]
```

```csharp
// Personクラス (C#)
public class Person
{
    public string Name { get; set; }
    public int Age { get; set; }
    public string Gender { get; set; } // "Male" or "Female"

    public Person(string name, int age, string gender)
    {
        Name = name;
        Age = age;
        Gender = gender;
    }

    public override string ToString()
    {
        return $"Person{{Name='{Name}', Age={Age}, Gender='{Gender}'}}";
    }
}

// データ準備 (C#)
List<Person> people = new List<Person>
{
    new Person("Alice", 25, "Female"),
    new Person("Bob", 30, "Male"),
    new Person("Charlie", 35, "Male"),
    new Person("Diana", 28, "Female"),
    new Person("Eve", 40, "Female"),
    new Person("Frank", 45, "Male")
};

// --- 伝統的なforeachループ (C#) ---
List<string> namesOfAdultMalesForEach = new List<string>();
foreach (var person in people)
{
    if (person.Age >= 30 && person.Gender == "Male")
    {
        namesOfAdultMalesForEach.Add(person.Name);
    }
}
Console.WriteLine($"For-each (C#): {string.Join(", ", namesOfAdultMalesForEach)}"); // Bob, Charlie, Frank

// --- LINQ (C#) ---
List<string> namesOfAdultMalesLinq = people
    .Where(person => person.Age >= 30)
    .Where(person => person.Gender == "Male")
    .Select(person => person.Name)
    .ToList();
Console.WriteLine($"LINQ (C#): {string.Join(", ", namesOfAdultMalesLinq)}"); // Bob, Charlie, Frank
```

---
**AIからのコメント**:

-   **伝統的なループ (`for`/`foreach`)**:
    -   データを「どのように」処理するか（ループの開始、条件分岐、結果リストへの追加）という「手続き」が記述されています。
    -   処理の流れを一つずつ追う必要があり、複雑な条件や複数の操作が加わると、コードが長くなり、意図が把握しにくくなる傾向があります。

-   **Stream API (Java) / LINQ (C#)**:
    -   データを「どのように変形したいか」という「意図」が明確に記述されています。
    -   `filter` (Java) / `Where` (C#) で条件を絞り込み、`map` (Java) / `Select` (C#) でデータを変換するという一連の操作が、まるでパイプラインのように連続して表現されています。
    -   結果として、コードが非常に簡潔になり、可読性が向上します。処理の意図が明確なため、後の保守作業も容易になります。

---

## 2. Java vs C#：最新機能を交えたコレクション操作の比較

AIの回答、素晴らしいね！ `for`ループと`Stream`/`LINQ`の記述スタイルの違い、そして意図の明確さという点で、大きな違いがあることを理解できたかな。

ここからは、さらに踏み込んで、もう少し複雑な操作や、JavaとC#それぞれの最新機能を交えながら比較してみよう。

### **2-1. 高度な集計とグループ化**

ただ抽出するだけでなく、「年齢別にグループ化して、各グループの名前をカンマ区切りで表示したい」といった、もう少し複雑な要件はどうだろう？

```java
// Java (Stream API)
import java.util.Map;
import java.util.stream.Collectors;

// ... Personクラスとpeopleリストの定義は省略 ...

Map<Integer, String> namesByAgeGroupJava = people.stream()
    .collect(Collectors.groupingBy( // 年齢でグループ化
        Person::getAge,
        Collectors.mapping(Person::getName, Collectors.joining(", ")) // 各グループの名前を結合
    ));
System.out.println("Names by age group (Java): " + namesByAgeGroupJava);
// 出力例: {35=Charlie, 40=Eve, 45=Frank, 25=Alice, 30=Bob, 28=Diana}
```

```csharp
// C# (LINQ)

// ... Personクラスとpeopleリストの定義は省略 ...

var namesByAgeGroupCSharp = people.GroupBy(person => person.Age) // 年齢でグループ化
                                .ToDictionary(
                                    group => group.Key, // キーは年齢
                                    group => string.Join(", ", group.Select(person => person.Name)) // 値はグループ内の名前を結合
                                );
Console.WriteLine($"Names by age group (C#): {{ {string.Join(", ", namesByAgeGroupCSharp.Select(kvp => $"{kvp.Key}={kvp.Value}"))} }}");
// 出力例: Names by age group (C#): { 25=Alice, 30=Bob, 35=Charlie, 28=Diana, 40=Eve, 45=Frank }
```

**シニアからのコメント**:
Javaの`Collectors.groupingBy`は、第2引数にさらに`Collector`を渡すことで、グループ内の要素をどのように集計するかを細かく制御できます。これは非常に強力な機能です。
C#のLINQでは`GroupBy`でグループ化した後、`ToDictionary`や`ToList`を使って、結果を任意の形に変換します。`string.Join`と`Select`の組み合わせもよく使われますね。どちらも宣言的に複雑な集計処理を記述できていることがわかります。

### **2-2. Java 21のレコードとStream API**

Java 16で導入され、Java 21で成熟した**レコード（Records）**は、`Stream`と非常に相性が良いです。不変のデータホルダーを簡潔に定義でき、Streamでデータを変換する際に活用できます。

```java
// Java 21: レコードの利用例
record PersonRecord(String name, int age, String gender) {} // Personクラスをより簡潔に定義

List<PersonRecord> peopleRecords = Arrays.asList(
    new PersonRecord("Alice", 25, "Female"),
    new PersonRecord("Bob", 30, "Male"),
    new PersonRecord("Charlie", 35, "Male")
);

// レコードを使ったStream操作
List<String> youngFemaleNames = peopleRecords.stream()
    .filter(p -> p.age() < 30 && p.gender().equals("Female")) // レコードのアクセサメソッドは自動生成される
    .map(PersonRecord::name)
    .toList(); // Java 16+ で導入された Listへの変換
System.out.println("Young Female Names (Java Record Stream): " + youngFemaleNames);
// 出力例: [Alice]
```

**シニアからのコメント**:
レコードを使うことで、`Person`のようなシンプルなデータクラスの定義が劇的に簡潔になります。`getName()`のようなゲッターも`name()`として自動生成されるため、Streamのラムダ式もスッキリ書けますね。
`toList()`メソッドはJava 16以降で導入され、`collect(Collectors.toList())`よりも簡潔にリストを作成できます。

### **2-3. C# 12のコレクション式とLINQの組み合わせ**

C# 12で導入された**コレクション式（Collection Expressions）**は、LINQの結果をより直感的に初期化するのに役立ちます。

```csharp
// C# 12: コレクション式の利用例

// ... Personクラスとpeopleリストの定義は省略 ...

// LINQの結果を直接コレクション式で初期化
List<string> adultMaleNamesCollectionExpression = [
    .. people.Where(p => p.Age >= 30 && p.Gender == "Male")
            .Select(p => p.Name)
];
Console.WriteLine($"Adult Male Names (C# 12 Collection Expression): {string.Join(", ", adultMaleNamesCollectionExpression)}");
// 出力例: Adult Male Names (C# 12 Collection Expression): Bob, Charlie, Frank

// 複数のLINQ結果を結合することも可能
List<string> combinedNames = [
    .. people.Where(p => p.Gender == "Female").Select(p => p.Name),
    "---",
    .. people.Where(p => p.Gender == "Male").Select(p => p.Name)
];
Console.WriteLine($"Combined Names (C# 12 Collection Expression): {string.Join(", ", combinedNames)}");
// 出力例: Combined Names (C# 12 Collection Expression): Alice, Diana, Eve, ---, Bob, Charlie, Frank
```

**シニアからのコメント**:
C# 12のコレクション式は、`IEnumerable<T>`なLINQの実行結果を直接`..`スプレッド要素として埋め込むことができるため、リストや配列の初期化が非常に柔軟かつ簡潔になります。コードの見た目がより一層洗練されますね。

## 3. 若手エンジニアへの一言：明日から使える「お作法」

ここまで見てきたように、`Stream`や`LINQ`は単なる「新しい書き方」ではなく、「より意図を明確に、保守性を高く、そして簡潔に」コードを書くための強力なツールです。

明日からすぐに実践できる「お作法」を伝授しましょう。

1.  **「何をしたいか」を最初に考えるべし！**
    `for`ループは「どう動かすか」の手続きですが、`Stream`/`LINQ`は「何をするか」の宣言です。
    -   フィルタリング（条件に合うものだけ残す）？ `filter` / `Where`
    -   変換（形を変える）？ `map` / `Select`
    -   集計（合計、平均、グループ化）？ `reduce`, `collect` / `Sum`, `Average`, `GroupBy`
    -   ソート？ `sorted` / `OrderBy`
    これらを意識するだけで、自然と`Stream`/`LINQ`の思考に近づけます。

2.  **パイプライン（連鎖）で書くべし！**
    複数の操作を繋げていくことで、データの流れが一本道のように見え、非常に読みやすくなります。一つ一つの操作が小さく、明確な役割を持つため、デバッグもしやすくなります。

3.  **まずは真似から入るべし！**
    最初から完璧に使いこなす必要はありません。先輩たちのコードを読んで、「あ、この場面では`filter`を使っているな」「ここで`map`して型を変えているな」という使われ方を体感してください。写経も効果的です。

4.  **副作用のないコードを意識するべし！**
    `Stream`/`LINQ`は基本的に、元のコレクションを変更せず、新しいコレクションを生成します（非破壊的）。この「イミュータブル（不変）」な考え方は、バグの少ない、予測しやすいコードを書く上で非常に重要です。

5.  **複雑になったら分割する勇気を持つべし！**
    長すぎるメソッドチェーンは、かえって可読性を損ねます。適切なところで一時変数に格納したり、独立したメソッドに切り出したりすることも、保守性を高める上で重要です。

6.  **Optional (Java) / Null許容型 (C#) と組み合わせるべし！**
    特にJavaの`Optional`は`Stream`と非常に相性が良いです。`null`の可能性のある値の扱いを明示的にすることで、`NullPointerException`のような実行時エラーを減らし、より堅牢なコードになります。C#でも`FirstOrDefault()`の戻り値が`null`になりうることを意識し、適切にハンドリングしましょう。

### **最後に**

コレクション操作は、あらゆるアプリケーションで頻繁に行われる基本中の基本です。
`Stream`や`LINQ`をマスターすることは、皆さんが「動けばいい」段階から「品質の高いコード」を書けるエンジニアへと成長するための、大きな一歩となるでしょう。

最初は難しく感じるかもしれませんが、慣れてしまえばこれほど便利で、読みやすいコードが書けるようになる強力な味方はいません。ぜひ、今日から意識して使ってみてください。

困ったらいつでも相談してくださいね！
それでは、良きプログラミングライフを！🎓✨