# Zenn Content 自動投稿システム

GitHub ActionsとGemini AIを使って、Zennの記事を自動生成・投稿するシステムです。

---

## 自動化の流れ

```
GitHub Actions実行（毎日自動 or 手動）
    ↓
Gemini AIが記事ファイルを自動生成
    ↓
GitHubリポジトリにプッシュされる
    ↓
ZennがGitHubの変更を検知して自動デプロイ
    ↓
Zennに記事が投稿される
```

---

## フォルダ構成

```
zenn-content/
├── .github/
│   └── workflows/
│       └── daily-post.yml        # GitHub Actionsの設定ファイル
├── articles/
│   ├── log-YYYY-MM-DD.md         # 自動生成される記事（思考プロセス系）
│   ├── ref-YYYY-MM-DD.md         # 自動生成される記事（Wiki系）
│   ├── process/
│   │   └── daily_article.py      # 思考プロセス記事を生成するスクリプト
│   └── wiki/
│       └── wiki_generator.py     # Wiki記事を生成するスクリプト
└── README.md
└── README2.md
```

---

## 初期セットアップ

### 1. 必要なAPIキーの設定

GitHubリポジトリの Settings → Secrets and variables → Actions に以下を追加します。

| キー名 | 内容 |
|--------|------|
| `GEMINI_API_KEY` | Google AI StudioのAPIキー |

### 2. ZennとGitHubの連携

1. [Zenn](https://zenn.dev) にログイン
2. 「GitHub連携」→「リポジトリ設定」でこのリポジトリを連携

### 3. Google Cloud課金の有効化

Gemini APIの無料枠を超えた場合に必要です。
[Google Cloud Console](https://console.cloud.google.com) で課金アカウントをリンクしてください。

---

## 記事を公開する方法

自動生成された記事は `published: false`（下書き状態）になっています。
公開する場合は以下の手順で変更してください。

### 1. 記事ファイルを開く

```
articles/log-YYYY-MM-DD.md
```

### 2. Front Matterを変更する

```yaml
# 変更前（下書き）
published: false

# 変更後（公開）
published: true
```

### 3. コミット＆プッシュ

```bash
git add .
git commit -m "publish article"
git push
```

プッシュ後、ZennのデプロイページでDeployが成功すれば記事が公開されます。

---

## 手動で記事を生成する方法

GitHub Actionsの画面で手動実行できます。

1. GitHubの「**Actions**」タブを開く
2. 「**Automatic Zenn Post**」を選択
3. 「**Run workflow**」ボタンをクリック

---

## トラブルシューティング

### GitHub Actionsが失敗する場合

| エラー | 原因 | 対処法 |
|--------|------|--------|
| `404 NOT_FOUND` | モデル名が間違っている | `gemini-2.0-flash` に変更 |
| `429 RESOURCE_EXHAUSTED` | APIのレート制限超過 | スクリプト間に `sleep 60` を追加 |
| `GEMINI_API_KEY is not set` | APIキーが未設定 | GitHub Secretsを確認 |

### Zennのデプロイが失敗する場合

| エラー | 原因 | 対処法 |
|--------|------|--------|
| `FrontMatterが見つかりません` | 記事ファイルの形式が不正 | 古いファイルを削除して再生成 |

---

## 使用技術

- **GitHub Actions**: 毎日の自動実行
- **Gemini AI**: 記事の自動生成（`gemini-2.0-flash`）
- **Python**: 記事生成スクリプト
- **Zenn CLI**: GitHubとZennの連携
