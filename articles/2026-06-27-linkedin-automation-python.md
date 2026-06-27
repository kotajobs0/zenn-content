---
title: "GeminiとClaudeを直列につないだSNS投稿生成パイプラインを作った"
emoji: "🤖"
type: "tech"
topics: ["python", "ai", "claude", "gemini", "自動化"]
published: false
---

## はじめに

こんにちは。AIエンジニアをしている長井洸太です。

「LLMを2つ直列につないだら何が変わるか」を試したくて、LinkedIn投稿の自動生成スクリプトを作りました。

単一モデルでも動くはずなのにあえて2段構成にしたのは、**役割を分けることでプロンプトの複雑度を下げられる**という仮説を検証したかったからです。結論から言うと、この仮説は正しかったです。

パイプライン全体の流れはこうです。

```
[収集]
  Hacker News API + RSS（Anthropic/Google DeepMind等）
          ↓
[要約・絞り込み]   ← Gemini 2.5 Flash
          ↓
[投稿文生成 × 3パターン]  ← Claude Sonnet
          ↓
[画像生成]   ← DALL-E gpt-image-1（スタイルをランダム選択）
          ↓
  Markdown保存
```

---

## なぜ1モデルで完結させなかったか

最初は Claude 1本で「ニュース要約→投稿文生成」を通しでやろうとしました。プロンプトはこうなります。

```
・複数ソースのニュースを収集した結果（大量テキスト）
・今週のテーマに合わせて3件に絞り込んでください
・その3件をもとに、以下の制約で投稿文を3パターン作ってください
  - Markdown記号を使わない
  - 曖昧語を使わない
  - 文字数は280〜380文字
  - ハッシュタグは3つ以内
  ...
```

これが **1つのプロンプトに「選定」と「生成」が混在する** 状態で、出力が安定しませんでした。選定件数がずれる、制約が守られないケースが出てきました。

役割を分けると、それぞれのプロンプトが単一責務になります。

```
Gemini：「3件に絞り込んでください」だけ
Claude：「この3件のニュースをもとに投稿文を書いてください」だけ
```

Claude に渡るコンテキストが「整理済みの3件」になるので、制約の追従率が上がりました。

---

## Gemini側の実装：収集と絞り込み

ニュース収集は Hacker News の公式 Firebase API と feedparser でまとめています。

```python
import feedparser
import requests
from google import genai

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def fetch_hacker_news(limit=5) -> list[str]:
    ids = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json", timeout=10
    ).json()[:80]
    results = []
    AI_KEYWORDS = ["ai", "llm", "gpt", "openai", "anthropic", "claude", "agent"]
    for sid in ids:
        item = requests.get(
            f"https://hacker-news.firebaseio.com/v0/item/{sid}.json", timeout=5
        ).json()
        if item and any(kw in item.get("title", "").lower() for kw in AI_KEYWORDS):
            results.append(f"- {item['title']}  ({item.get('url', '')})")
        if len(results) >= limit:
            break
    return results

def fetch_rss(url: str, limit: int = 3) -> list[str]:
    feed = feedparser.parse(url)
    return [f"- {e.get('title','')}  ({e.get('link','')})"
            for e in feed.entries[:limit]]
```

Gemini への絞り込み指示はこうしています。

```python
def summarize_news(raw_sources: str, theme: str) -> str:
    prompt = f"""
以下のAIニュースから、今週のテーマに最も関連する3件を選んでください。

【今週のテーマ】{theme}
【収集済みニュース】
{raw_sources}

【出力形式（プレーンテキストのみ）】
タイトル：〇〇
URL：〇〇
概要：1行
"""
    resp = gemini_client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    return resp.text.replace("**", "")
```

`.replace("**", "")` はGeminiが勝手にMarkdownを混入させることがあるための後処理です。出力形式を「プレーンテキストのみ」と明示していても混入するケースがあります。

週テーマのローテーションは `isocalendar()` の週番号を使います。

```python
WEEKLY_THEMES = [
    {"theme": "AI × 医療・ヘルスケア"},
    {"theme": "AI × 法律・教育"},
    {"theme": "AI × ビジネス・経営"},
    {"theme": "AI × クリエイティブ"},
]
week_index = datetime.now().isocalendar()[1] % 4
current_theme = WEEKLY_THEMES[week_index]["theme"]
```

---

## Claude側の実装：投稿文生成

3つの投稿パターンをデータとして定義し、ループで生成します。

```python
import anthropic

claude_client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

POST_PATTERNS = [
    {
        "name": "反論型",
        "day": "月曜向け",
        "rule": """
冒頭1行（20文字以内）：通説を真っ向否定する断言
本文：
  1段落目 - ニュースの具体的な数字・事実で根拠を示す
  2段落目 - 実務視点で一段深い本質を述べる
  3段落目 - 読者への問いかけ
禁止：「かもしれない」などの曖昧語、Markdown記号（**など）
文字数：280〜380文字（ハッシュタグ含む）
""",
    },
    {
        "name": "数字・リスト型",
        "day": "水曜向け",
        "rule": """
冒頭1行：具体的な数字を含むフック
各項目：[絵文字] タイトル → 数字・ビフォーアフターを1〜2行
文字数：320〜420文字、ハッシュタグ3つ以内
""",
    },
    {
        "name": "問題提起型",
        "day": "金曜向け",
        "rule": """
冒頭1行：立ち止まらせる一文
1段落目：ニュースの語られ方
2段落目：実務視点の深い問い（数字・具体例付き）
3段落目：読者へ問いを委ねて終える
文字数：300〜400文字、ハッシュタグ3つ以内
""",
    },
]

def generate_post(news_summary: str, pattern: dict) -> str:
    prompt = f"""
あなたはLinkedIn向けの投稿文ライターです。

【今週のAIニュース】
{news_summary}

【投稿スタイル：{pattern['name']}（{pattern['day']}）】
{pattern['rule']}

【共通制約】
・URLは本文に含めない
・Markdown記号（**など）は一切使わない
・投稿文のみ出力。前置き・後置きなし。

投稿文：
"""
    resp = claude_client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text.strip()
```

パターンをループするときはこうです。

```python
results = []
for pattern in POST_PATTERNS:
    text = generate_post(news_summary, pattern)
    results.append({"pattern": pattern["name"], "text": text})
```

---

## DALL-E：スタイルのランダム選択

毎回同じ見た目にならないよう、パターンごとにスタイルのプールを用意してランダム選択しています。

```python
import random
from openai import OpenAI

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

IMAGE_STYLE_POOLS: dict[str, list[str]] = {
    "反論型": [
        "LinkedIn-optimised professional portrait: confident Japanese woman mid-20s, "
        "navy blazer, minimal desk, direct eye contact. Studio lighting. 16:9, no text.",
        "LinkedIn-optimised environmental portrait: Japanese woman mid-20s at "
        "floor-to-ceiling windows, arms crossed, city skyline. 35mm f/2. 16:9, no text.",
        "LinkedIn-optimised action portrait: Japanese woman mid-20s at whiteboard, "
        "marker in hand. Bright workshop room. 16:9, no text.",
    ],
    # 数字・リスト型、問題提起型も同様に3スタイル
}

def generate_image(pattern_name: str, post_text: str, output_path: Path) -> bool:
    pool = IMAGE_STYLE_POOLS.get(pattern_name, [])
    style = random.choice(pool) if pool else ""

    try:
        resp = openai_client.images.generate(
            model="gpt-image-1",
            prompt=f"{style} Theme: {post_text[:100]}...",
            size="1536x1024",
            n=1,
        )
        item = resp.data[0]
        # gpt-image-1 は b64_json で返ることがある
        img_data = (
            base64.b64decode(item.b64_json) if item.b64_json
            else requests.get(item.url, timeout=30).content
        )
        output_path.write_bytes(img_data)
        return True
    except Exception as e:
        print(f"  [WARN] 画像生成失敗: {e}")
        return False
```

`gpt-image-1` は `url` と `b64_json` の両方のレスポンス形式がありえるため、どちらにも対応しています。`url` を期待していると本番で詰まるポイントです。

---

## 実装して気づいたこと

**直列2段構成にして変わったこと：**

単一プロンプトで書いていたころは「制約を守る」か「ニュースの選定精度」かのトレードオフがありました。2段にすることでそれぞれが単一責務になり、プロンプトのデバッグが楽になりました。どちらかの出力がおかしいとき、原因の切り分けも速いです。

**Geminiの後処理が必要な理由：**

`generate_content` は `response_mime_type="text/plain"` を指定しても `**` が混入するケースがあります。後続のClaudeプロンプトに混入するとアウトプットに影響するため、受け取り側で除去しています。

**次にやること：**

- GitHub Actions で曜日ごとに自動実行し、結果を Slack 通知
- LinkedIn API は第三者投稿に制限があるため、最終投稿は人間が行う構成を維持する

---

## まとめ

- LLMを役割で分けると、それぞれのプロンプトが単純になって制約追従率が上がる
- Gemini 2.5 Flash は絞り込み・要約のような「大量入力→短い出力」に向いている
- Claude Sonnet は文字数・文体・禁止表現など細かい制約付き生成に向いている
- `gpt-image-1` のレスポンスは `url` と `b64_json` の両形式に対応しておく必要がある

---

## おわりに

AIエンジニア / 個人事業主として、Gemini×Claude×DALL-Eを使った自動化パイプラインの実装記録をZennで発信しています。

X（[@kotajobs0](https://x.com/kotajobs0)）でも毎日AI活用の話を投稿しています。よかったらフォローしてください。

---

*関連記事：[LinkedIn投稿自動化（Qiita版・詳細コード）](https://qiita.com/kotajobs0/items/c492d00459d643434b73)*
