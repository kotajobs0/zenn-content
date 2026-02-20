import os
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

def get_ai_response(prompt):
    # 最新モデルを指定。'models/' は付けても付けなくても動作しますが、まずはシンプルに指定します。
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

def create_prompt():
    return """
あなたは日本を代表するシニアエンジニアとして、若手社員（Java/C#初心者）に向けて「エンジニアの思考プロセス」を伝えるZenn記事をMarkdownで書いてください。

## ターゲット
- 入社1-3年目のJava/C#エンジニア
- 「動けばいい」から「保守性の高いコード」へのステップアップを目指している層

## 内容の構成
1. **今回のテーマ**: 【リファクタリング】または【エラー解消デバッグ】から1つ選択。
2. **AIとの対話記録**: 
   - 「若手からの相談」→「シニアのあなたの思考」→「AI(Gemini)への指示」→「AIの回答」という流れを詳しく。
3. **Java vs C# 実装比較**: 
   - 最新機能（Java 21 / C# 12など）を交えて比較。
4. **若手への一言**: 明日から使える「お作法」のアドバイス。

## Zenn用Front Matter
---
title: "【Log】AIとの対話で学ぶ：[テーマ名]"
emoji: "🎓"
type: "tech"
topics: ["java", "csharp", "新人教育", "ai", "思考プロセス"]
published: false
---
"""

def main():
    if not GOOGLE_API_KEY:
        print("Error: GEMINI_API_KEY is not set.")
        return

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
    date_str = now.strftime('%Y-%m-%d_%H%M%S')
    filename = f"log-{date_str}.md"

    # 5. 最終的な保存先フルパス
    full_save_path = os.path.join(output_dir, filename)

    with open(full_save_path, "w", encoding="utf-8") as f: # 計算したフルパスを使う！
        f.write(article_content)
    
    print(f"Success: {filename} has been created!")

if __name__ == "__main__":
    main()