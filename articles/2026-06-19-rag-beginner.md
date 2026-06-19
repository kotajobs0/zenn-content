---
title: "RAGって何？仕組みから精度改善まで初心者向けに解説【Dify・Re-rank・Langfuse】"
emoji: "🔍"
type: "tech"
topics: ["rag", "llm", "dify", "python", "生成ai"]
published: true
---

## はじめに

こんにちは。ITフィールドセールスをしている長井洸太です。

最近、企業向けのAI導入案件で「RAG」という言葉をよく耳にします。

「ChatGPTは知っているけどRAGは？」という方も多いと思うので、**仕組みの解説から構築・精度改善まで**まとめました。

---

## RAGとは何か

**RAG（Retrieval-Augmented Generation）** とは、AIが回答を生成するときに「外部のドキュメントやデータベース」を検索して参照する仕組みです。

通常のLLMとの違いはこうです。

| | 通常のLLM | RAG |
|---|---|---|
| 参照するデータ | 学習データのみ | 学習データ + 外部ドキュメント |
| 最新情報 | 使えない | 使える |
| 社内文書 | 使えない | 使える |
| ハルシネーション | 多い | 少ない |

社内マニュアル・契約書・議事録などを読ませてQ&Aができるため、**企業の情報活用**に非常に相性が良いです。

---

## RAGの処理フロー

RAGは「事前準備フェーズ」と「質問応答フェーズ」に分かれます。

### 事前準備（インデックス作成）

```
① ドキュメント投入（PDF / テキスト / Webページ）
        ↓
② チャンク分割（文章を小さなブロックに切り分ける）
        ↓
③ ベクトル化（テキストを数値ベクトルに変換）
        ↓
④ ベクトルDBに保存（Chroma / FAISS / Pinecone）
```

### 質問応答（推論）

```
ユーザーの質問
        ↓
① 質問をベクトル化
        ↓
② ベクトルDBで類似検索（上位N件取得）
        ↓
③ Re-rank（関連度を再スコアリングして絞り込む）
        ↓
④ LLMに「文書 + 質問」を渡す
        ↓
回答生成
```

---

## Difyで手軽にRAGを構築する

[Dify](https://dify.ai/) はRAGアプリをGUIとAPIの両方で構築できるOSSプラットフォームです。コードを書かなくてもチャットボットUIが作れます。

### ローカル起動（Docker）

```bash
git clone https://github.com/langgenius/dify.git
cd dify/docker
docker compose up -d
```

`http://localhost` にアクセスするとセットアップ画面が表示されます。

### PythonからAPI呼び出し

```python
import requests

url = "http://localhost/v1/chat-messages"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
payload = {
    "inputs": {},
    "query": "有給申請の手順を教えてください",
    "response_mode": "blocking",
    "conversation_id": "",
    "user": "user-001"
}

response = requests.post(url, headers=headers, json=payload)
print(response.json()["answer"])
```

---

## RAG精度改善の3つのポイント

RAGを動かすだけなら簡単ですが、**実用レベルの精度を出す**には工夫が必要です。

### 1. チャンク戦略

ドキュメントをどう分割するかで精度が大きく変わります。

| 戦略 | 概要 | 向いているケース |
|---|---|---|
| Fixed Size | 固定文字数で分割 | シンプルな構造のドキュメント |
| Semantic | 意味の区切りで分割 | 自然文が多い文書 |
| Hierarchical | 大→小の階層構造で保持 | 章立てのある長文書 |

**チャンクサイズの目安**：512〜1024トークン。小さすぎると文脈が失われ、大きすぎるとノイズが増えます。

### 2. Retrieval改善 + Re-rank

検索で取得した候補（例：上位20件）を、より精密なモデルで再スコアリングして上位5件に絞ります。

```python
import cohere

co = cohere.Client("YOUR_COHERE_API_KEY")

results = co.rerank(
    query="有給申請の手順",
    documents=retrieved_chunks,
    top_n=5,
    model="rerank-multilingual-v3.0"
)
```

他にも以下のRetrieval改善手法があります。

- **Hybrid Search**：ベクトル検索 + キーワード検索（BM25）を組み合わせる
- **Multi-query**：質問を複数バリエーションに変換して検索精度を上げる

### 3. LLMOps：Langfuseで品質モニタリング

本番運用では「どの質問で精度が落ちているか」を可視化することが重要です。

[Langfuse](https://langfuse.com/) を使うと、以下が可視化できます。

- 各クエリのレイテンシ
- 使用トークン数・コスト
- 取得されたチャンクの内容
- LLMの入出力ログ

```python
from langfuse import Langfuse

langfuse = Langfuse(
    public_key="YOUR_PUBLIC_KEY",
    secret_key="YOUR_SECRET_KEY"
)

trace = langfuse.trace(name="rag-query")
span = trace.span(name="retrieval", input={"query": user_query})
# 検索処理...
span.end(output={"chunks": retrieved_chunks})
```

---

## まとめ

RAGの精度改善は「取得（Retrieval）」と「生成（Generation）」の両方に手を入れる必要があります。

| フェーズ | 手法 |
|---|---|
| 取得 | チャンク戦略・Hybrid Search・Re-rank |
| 生成 | プロンプト改善・Few-shot例示 |
| 運用 | Langfuseでモニタリング |

まずは **DifyをDockerで立ち上げてPDFを投入する** ところから始めると、全体の流れがつかみやすいです。

---

ITフィールドセールスの視点から、AI・自動化について発信しています。フォローや「いいね」していただけると励みになります。
