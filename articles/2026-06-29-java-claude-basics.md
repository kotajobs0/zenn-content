---
title: "Javaエンジニアが初めてClaudeを使うときに最初に知っておくべき3つのこと"
emoji: "☕"
type: "tech"
topics: ["java", "claude", "ai", "api", "初心者"]
published: true
---

こんにちは。エンジニアをしている長井洸太です。

普段はLinkedIn・Instagram・Qiitaで「セールスがPythonで業務自動化した」系の話を書いているのですが、今回はちょっと違う切り口で。

社内のJavaエンジニアと話していてよく聞くのが、こういう声です。

> 「Claudeって結局なにもの？どうやって使うの？」
> 「ChatGPTとなにが違うの？」
> 「API叩くのって難しい？」

試してみたいけど、最初の一歩が見えない——そんな人向けに、今回は「Javaエンジニアが最初に知っておくべき3つのこと」を整理しました。

---

## そもそも「Claude API」とは何か

ClaudeはAnthropicという会社が作っているAIです。ChatGPTと同じカテゴリですが、**API（プログラムから呼び出せるインターフェース）が公開されていて、自分のアプリに組み込める**のが大きな特徴です。

つまり「Claudeをただ使う」じゃなくて、「ClaudeをJavaのコードから呼び出して、自分のサービスの一部にする」ことができます。

前置きはここまでにして、本題に入ります。

---

## 1. モデルは3種類ある——用途で使い分けるのがコツ

Claudeには現在、主に3つのモデルがあります。

| モデル | 特徴 | 向いてる用途 |
|--------|------|------------|
| `claude-haiku-4-5` | 速い・安い | 分類・短文生成・チャット |
| `claude-sonnet-4-6` | バランス型 | 一般的なタスク全般 |
| `claude-opus-4-8` | 高精度・深い推論 | 複雑な判断・コードレビュー |

Javaでたとえると、こんなイメージです。

```
Haiku  ≈ HashMapへの単純なlookup（速い、安い）
Sonnet ≈ 一般的なビジネスロジック（バランスが良い）
Opus   ≈ 複雑なアルゴリズム・最適化処理（時間はかかるが高精度）
```

Claudeに「このモデルどれ使えばいい？」と直接聞いてみました。

```
私：「Javaのコードに軽いバリデーション機能を追加したい。どのモデルが向いてる？」

Claude：「バリデーションの判断ロジックがシンプルなら、Haikuで十分です。
入力値の種類を分類して、エラーメッセージを返すだけなら、速度と
コストのバランスが良いHaikuが最適です。
複雑なビジネスルールが絡むなら、Sonnetにするとより安定します。」
```

**最初はSonnetを使ってみて、レスポンス速度やコストが気になったらHaikuに下げる**というアプローチが実務では多いです。

---

## 2. プロンプト設計はメソッドの引数定義と同じ考え方

これがJavaエンジニアに一番刺さるポイントだと思っています。

Claudeへのリクエストは、本質的には「関数呼び出し」と同じです。

```java
// Javaのメソッド定義
public String reviewCode(String code, String language, int maxLength) {
    // ...
}
```

```
// Claudeへのプロンプト（同じ構造）
あなたはシニアエンジニアです。（役割）
以下のコードをレビューしてください。（処理内容）
- 言語: Java
- コード: [コードをここに貼る]
- 出力は200文字以内で。（制約）
```

どちらも「入力を明確に定義して、出力の形式を指定する」という構造は同じです。

Claudeにこれを確認したら、こんな返答が来ました。

```
私：「プロンプト設計ってどう考えたらいいですか？」

Claude：「役割（Role）・タスク（Task）・制約（Constraint）・
出力形式（Output Format）の4つを明示するのが基本です。
Javaでいうと、メソッドのシグネチャとアノテーションで
何を受け取って何を返すかを宣言するイメージに近いです。」
```

たとえば「コードレビューをしてほしい」だけだと、どんな観点でどんな形式で返ってくるかが不定です。

```
# 曖昧なプロンプト（△）
このコードをレビューして。

# 明確なプロンプト（○）
あなたはJavaのシニアエンジニアです。
以下のコードを、セキュリティとパフォーマンスの観点でレビューしてください。
問題点を箇条書き3点以内でまとめ、それぞれに改善案を添えてください。

[コード]
```

**引数の型と戻り値の型を定義するように、プロンプトも構造化する**——この考え方が身につくと、Claudeの出力が格段に安定します。

---

## 3. JavaからClaude APIを叩く方法

ここが一番気になるところだと思います。

Claude APIはREST APIなので、JavaのHTTPクライアントで呼び出せます。Java 11以降なら標準の `HttpClient` でOKです。

### 必要なもの

1. Anthropicのアカウント（[console.anthropic.com](https://console.anthropic.com) で作成）
2. APIキー（コンソールで発行）

### 最小サンプルコード（Java 11+）

```java
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

public class ClaudeApiExample {

    private static final String API_KEY = System.getenv("CLAUDE_API_KEY");
    private static final String API_URL = "https://api.anthropic.com/v1/messages";

    public static void main(String[] args) throws Exception {
        String requestBody = """
            {
              "model": "claude-sonnet-4-6",
              "max_tokens": 1024,
              "messages": [
                {
                  "role": "user",
                  "content": "Javaのリストを逆順にする方法を教えてください。"
                }
              ]
            }
            """;

        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(API_URL))
            .header("Content-Type", "application/json")
            .header("x-api-key", API_KEY)
            .header("anthropic-version", "2023-06-01")
            .POST(HttpRequest.BodyPublishers.ofString(requestBody))
            .build();

        HttpResponse<String> response = client.send(
            request,
            HttpResponse.BodyHandlers.ofString()
        );

        System.out.println("Status: " + response.statusCode());
        System.out.println("Body: " + response.body());
    }
}
```

### レスポンスのJSONを解析する

上記のコードで返ってくるJSONはこんな形です。

```json
{
  "content": [
    {
      "type": "text",
      "text": "Javaでリストを逆順にするには...\n\nCollections.reverse(list); を使う方法が最もシンプルです。"
    }
  ],
  "model": "claude-sonnet-4-6",
  "usage": {
    "input_tokens": 20,
    "output_tokens": 80
  }
}
```

`content[0].text` に回答が入っています。JSONの解析にはJacksonやGsonを使うのが一般的です。

```java
// Jacksonを使った解析例（pom.xmlにjackson-databind追加が必要）
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

ObjectMapper mapper = new ObjectMapper();
JsonNode root = mapper.readTree(response.body());
String text = root.get("content").get(0).get("text").asText();
System.out.println("Claude: " + text);
```

### APIキーは環境変数で管理する

```bash
# Windows（PowerShell）
$env:CLAUDE_API_KEY = "sk-ant-..."

# macOS / Linux
export CLAUDE_API_KEY="sk-ant-..."
```

コードにAPIキーをベタ書きするのは絶対NGです。環境変数かシークレット管理ツールを使いましょう。

---

## やってみてわかったこと

### 「APIを叩く」こと自体はシンプル

Javaエンジニアが最初に「難しそう」と感じるのは、AIに対する漠然とした距離感だと思います。でも実際にやってみると、**Claude APIはただのREST APIです**。Javaで外部APIを叩いたことがあれば、コードはほぼそのままです。

### プロンプト設計が一番のハマりポイント

難しいのは「どう呼ぶか」より「何を渡すか」です。引数の設計が甘いと、期待した出力が返ってこない——これはAPIの問題じゃなくて、プロンプトの問題です。Javaのメソッド定義と同じように、入力と出力を明確にするクセをつけると、グッと安定します。

### モデルの使い分けはコスト感覚と直結する

Haikuは安くて速いですが、複雑な質問への回答が浅くなることがあります。Opusは深い推論ができますが、コストが高い。プロダクションで使うときは「どのタスクにどのモデルを使うか」の設計がコストに直結します。

---

## 若手Javaエンジニアへ

「AIをサービスに組み込む」というのは、もはや特別なスキルじゃなくなってきました。Claude APIを叩けるJavaエンジニアは、今後ますます価値が上がると思っています。

今回紹介した3つは、どれもJavaエンジニアがすでに持っている考え方の延長線上にあります。

- モデル選び ≒ ライブラリ選定
- プロンプト設計 ≒ メソッドのシグネチャ定義
- API呼び出し ≒ 外部REST APIの利用

まずは最小サンプルを動かしてみてください。「動いた」という体験が、次のステップへの一番の推進力になります。

---

## まとめ

| ポイント | まとめ |
|--------|------|
| モデル選び | まずSonnetから試して、必要に応じてHaikuかOpusに切り替える |
| プロンプト設計 | 役割・タスク・制約・出力形式を明示する（メソッド定義と同じ） |
| API呼び出し | Java 11の`HttpClient`で叩ける。JSONレスポンスの`content[0].text`を取り出す |

---

## おわりに

Javaエンジニアがどんな観点でAIを見ているのか、また聞かせてください。記事の感想や「こういうテーマで書いてほしい」という声もお待ちしています。

X（Twitter）で毎日ITセールスやAI活用の話を投稿しています。ぜひつながりましょう！

[@kotajobs0](https://x.com/kotajobs0)

---

*参考：Claude API公式ドキュメント https://docs.anthropic.com*
