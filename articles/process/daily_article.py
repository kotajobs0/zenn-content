import os
import sys
import random
import re
import time
import subprocess
from pathlib import Path
import datetime
from dotenv import load_dotenv
import google.genai as genai

env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options={'api_version': 'v1beta'}
)

ARTICLES_DIR = Path(__file__).resolve().parent.parent

THEMES = [
    "リファクタリング",
    "エラー解消デバッグ",
    "単体テスト設計",
    "ログ設計・例外処理",
    "デザインパターン（Strategy）",
    "デザインパターン（Factory）",
    "デザインパターン（Observer）",
    "コードレビューの作法",
    "命名規則とコードの可読性",
    "非同期処理・async/await",
    "コレクション操作（Stream/LINQ）",
    "依存性注入（DI）",
    "インターフェース設計",
    "不変オブジェクト（Immutable）",
    "Null安全・Optional",
    "ジェネリクスの活用",
    "パフォーマンスチューニング入門",
    "SQLとORMの使い分け",
    "REST API設計の基礎",
    "セキュリティ基礎（インジェクション対策）",
    "データ構造の選択（List vs Map vs Set）",
    "再帰処理の考え方",
    "継承vs合成の設計判断",
    "トランザクション管理の基礎",
    "バリデーション設計",
]

def theme_to_slug(theme: str) -> str:
    """テーマ名をZenn用スラグに変換する（英字・数字・ハイフンのみ）"""
    mapping = {
        "リファクタリング": "refactoring",
        "エラー解消デバッグ": "error-debug",
        "単体テスト設計": "unit-test",
        "ログ設計・例外処理": "logging-exception",
        "デザインパターン（Strategy）": "design-pattern-strategy",
        "デザインパターン（Factory）": "design-pattern-factory",
        "デザインパターン（Observer）": "design-pattern-observer",
        "コードレビューの作法": "code-review",
        "命名規則とコードの可読性": "naming-readability",
        "非同期処理・async/await": "async-await",
        "コレクション操作（Stream/LINQ）": "stream-linq",
        "依存性注入（DI）": "dependency-injection",
        "インターフェース設計": "interface-design",
        "不変オブジェクト（Immutable）": "immutable-object",
        "Null安全・Optional": "null-safety-optional",
        "ジェネリクスの活用": "generics",
        "パフォーマンスチューニング入門": "performance-tuning",
        "SQLとORMの使い分け": "sql-orm",
        "REST API設計の基礎": "rest-api-design",
        "セキュリティ基礎（インジェクション対策）": "security-injection",
        "データ構造の選択（List vs Map vs Set）": "data-structure",
        "再帰処理の考え方": "recursion",
        "継承vs合成の設計判断": "inheritance-vs-composition",
        "トランザクション管理の基礎": "transaction-management",
        "バリデーション設計": "validation-design",
    }
    return mapping.get(theme, re.sub(r"[^a-z0-9-]", "-", theme.lower())[:30])


def get_ai_response(prompt, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            text = response.text
            start_index = text.find('---')
            if start_index != -1:
                before = text[:start_index].replace('```markdown', '').replace('```yaml', '').replace('```', '')
                text = before + text[start_index:]
            return text.strip()
        except Exception as e:
            print(f"Error (attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                time.sleep(5)
            else:
                print("Max retries reached. Exiting.")
                sys.exit(1)


def create_prompt(theme: str) -> str:
    return f"""
あなたは日本を代表するシニアエンジニアとして、若手社員（Java/C#初心者）に向けて「エンジニアの思考プロセス」を伝えるZenn記事をMarkdownで書いてください。

## ターゲット
- 入社1-3年目のJava/C#エンジニア
- 「動けばいい」から「保守性の高いコード」へのステップアップを目指している層

## 今回のテーマ
【{theme}】

## 内容の構成
1. **AIとの対話記録**:
   - 「若手からの相談」→「シニアのあなたの思考」→「AI(Gemini)への指示」→「AIの回答」という流れを詳しく。
2. **Java vs C# 実装比較**:
   - 最新機能（Java 21 / C# 12など）を交えて比較。
3. **若手への一言**: 明日から使える「お作法」のアドバイス。

## Zenn用Front Matter
記事の先頭に以下をそのまま出力してください（バッククォートで囲まない）:

---
title: "【Log】AIとの対話で学ぶ：{theme}"
emoji: "🎓"
type: "tech"
topics: ["java", "csharp", "新人教育", "ai", "思考プロセス"]
published: true
---
""".strip()


def git_push(repo_dir: Path, filepath: Path, commit_msg: str):
    """記事をgit add → commit → pushする"""
    try:
        subprocess.run(["git", "add", str(filepath)], cwd=repo_dir, check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=repo_dir, check=True)
        subprocess.run(["git", "push", "--set-upstream", "origin", "main"], cwd=repo_dir, check=True)
        print("✅ GitHubにpush完了 → Zennに自動反映されます")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ git操作でエラー: {e}")


def main():
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY is not set.")
        sys.exit(1)

    theme = random.choice(THEMES)
    print(f"テーマ: 【{theme}】 の記事を生成中...")

    prompt = create_prompt(theme)
    article_content = get_ai_response(prompt)

    today = datetime.datetime.now().strftime('%Y%m%d')
    slug = f"log-{today}-{theme_to_slug(theme)}"
    filename = f"{slug}.md"
    save_path = ARTICLES_DIR / filename

    # 同名ファイルが既にあれば別のテーマを選び直す
    if save_path.exists():
        print(f"⚠️ {filename} は既に存在します。別のテーマで再生成してください。")
        sys.exit(1)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(article_content)

    print(f"✅ 記事保存: {save_path}")

    repo_dir = ARTICLES_DIR.parent
    git_push(repo_dir, save_path, f"feat: Zenn記事追加「{theme}」")


if __name__ == "__main__":
    main()
