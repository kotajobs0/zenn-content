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
    "コレクション操作（List・Map・Set）",
    "ファイルI/O操作",
    "日付・時刻操作",
    "文字列操作",
    "正規表現の使い方",
    "例外処理パターン",
    "ロギング実装",
    "HTTP通信・REST APIクライアント",
    "JSON・XMLのパース",
    "データベース接続・JDBC/ADO.NET",
    "トランザクション管理",
    "スレッド・並行処理",
    "非同期処理・async/await",
    "ラムダ式・関数型プログラミング",
    "Stream API / LINQ",
    "ジェネリクス",
    "リフレクション",
    "依存性注入（DI）コンテナ",
    "単体テスト（JUnit/NUnit）",
    "モックの使い方（Mockito/Moq）",
    "ビルドツール（Maven/Gradle/MSBuild）",
    "設定ファイル管理（properties/appsettings）",
    "環境変数の扱い方",
    "暗号化・ハッシュ処理",
    "バリデーション実装",
]

def theme_to_slug(theme: str) -> str:
    mapping = {
        "コレクション操作（List・Map・Set）": "collection-list-map-set",
        "ファイルI/O操作": "file-io",
        "日付・時刻操作": "datetime-operation",
        "文字列操作": "string-operation",
        "正規表現の使い方": "regex",
        "例外処理パターン": "exception-handling",
        "ロギング実装": "logging",
        "HTTP通信・REST APIクライアント": "http-rest-client",
        "JSON・XMLのパース": "json-xml-parse",
        "データベース接続・JDBC/ADO.NET": "database-jdbc-adonet",
        "トランザクション管理": "transaction",
        "スレッド・並行処理": "thread-concurrency",
        "非同期処理・async/await": "async-await",
        "ラムダ式・関数型プログラミング": "lambda-functional",
        "Stream API / LINQ": "stream-linq",
        "ジェネリクス": "generics",
        "リフレクション": "reflection",
        "依存性注入（DI）コンテナ": "di-container",
        "単体テスト（JUnit/NUnit）": "junit-nunit",
        "モックの使い方（Mockito/Moq）": "mockito-moq",
        "ビルドツール（Maven/Gradle/MSBuild）": "build-tools",
        "設定ファイル管理（properties/appsettings）": "config-management",
        "環境変数の扱い方": "environment-variables",
        "暗号化・ハッシュ処理": "encryption-hash",
        "バリデーション実装": "validation",
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
あなたは、チームの技術標準を策定するリードエンジニアとして、若手が「そのまま実行できる」Zenn形式の技術リファレンス（Wiki）を書いてください。

## 今回のテーマ
【{theme}】

## 構成ルール
1. **即実行可能なコード (Ready-to-Run)**: import文から含めた完全なコード。
2. **バージョン・アップデート情報**: 言語バージョンアップに伴う推奨される書き方の変化。
3. **解説の深さ**: メモリ効率、スレッドセーフなどプロフェッショナルな視点。

## Zenn用Front Matter
記事の先頭に以下をそのまま出力してください（バッククォートで囲まない）:

---
title: "【Wiki】{theme} (Java/C# 実装リファレンス)"
emoji: "🛠️"
type: "tech"
topics: ["java", "csharp", "新人教育", "architecture", "wiki"]
published: true
---
""".strip()


def git_push(repo_dir: Path, filepath: Path, commit_msg: str):
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
    slug = f"wiki-{today}-{theme_to_slug(theme)}"
    filename = f"{slug}.md"
    save_path = ARTICLES_DIR / filename

    if save_path.exists():
        print(f"⚠️ {filename} は既に存在します。別のテーマで再生成してください。")
        sys.exit(1)

    with open(save_path, "w", encoding="utf-8") as f:
        f.write(article_content)

    print(f"✅ 記事保存: {save_path}")

    repo_dir = ARTICLES_DIR.parent
    git_push(repo_dir, save_path, f"feat: Zenn Wiki追加「{theme}」")


if __name__ == "__main__":
    main()
