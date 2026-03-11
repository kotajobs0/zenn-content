import os
import sys
import random
import time
from pathlib import Path
import datetime
from dotenv import load_dotenv
import google.genai as genai

# 1. スクリプトの場所からプロジェクトのルートパスを計算
#    (articles/process/ から2つ上の階層にある .env を指定)
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# 2. 環境変数から値を取り出す
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 3. クライアントを初期化
client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options={'api_version': 'v1beta'}
)

def get_ai_response(prompt, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            text = response.text

            # ---が最初に出てくる位置からを記事本文として取得
            start_index = text.find('---')
            if start_index != -1:
                text = text[start_index:]

            return text
        except Exception as e:
            print(f"Error (attempt {attempt}/{max_retries}): {e}")
            if attempt < max_retries:
                time.sleep(5)
            else:
                print("Max retries reached. Exiting.")
                sys.exit(1)

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

def create_prompt():
    theme = random.choice(THEMES)
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
---
title: "【Log】AIとの対話で学ぶ：{theme}"
emoji: "🎓"
type: "tech"
topics: ["java", "csharp", "新人教育", "ai", "思考プロセス"]
published: false
---
"""

def main():
    if not GOOGLE_API_KEY:
        print("Error: GOOGLE_API_KEY is not set.")
        sys.exit(1)

    print("Generating mentor-style article...")
    prompt = create_prompt()
    article_content = get_ai_response(prompt)

# 1. プログラム本体(daily_article.py)の絶対パスを取得
    # これにより、どこから実行しても「スクリプトがある場所」が基準になります
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path) # articles/process フォルダ

 # 2. パスを組み立てる
    # script_dir (articles/process) から
    # 一つ上の ".." (articles) に戻り、
    # その中の "data/logs" を指定する
    output_dir = os.path.normpath(os.path.join(script_dir, "..", "data", "logs"))
    
    print(f"DEBUG: スクリプトの場所 -> {script_dir}")
    print(f"DEBUG: 計算された保存先 -> {output_dir}")
    
    if os.path.exists(output_dir):
        print("✅ フォルダは見つかりました！")
    else:
        print("❌ フォルダが見つかりません。新しく作成します。")
    
    # 3. フォルダが存在しなければ作成
    os.makedirs(output_dir, exist_ok=True)

    # 4. ファイル名の生成
    now = datetime.datetime.now()
    date_str = now.strftime('%Y-%m-%d-%H%M%S')
    filename = f"log-{date_str}.md"

    # 5. 最終的な保存先フルパス
    full_save_path = os.path.join(output_dir, filename)

    with open(full_save_path, "w", encoding="utf-8") as f: # 計算したフルパスを使う！
        f.write(article_content)
    
    print(f"Success: {filename} has been created!")

if __name__ == "__main__":
    main()