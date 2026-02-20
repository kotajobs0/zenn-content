import os
import datetime
from google import genai

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# クライアントの初期化（api_version: 'v1' を指定）
client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options={'api_version': 'v1beta'}
)

def get_ai_response(prompt):
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

def create_wiki_prompt():
    return """
あなたは、チームの技術標準を策定するリードエンジニアとして、若手が「そのまま実行できる」Zenn形式の技術リファレンス（Wiki）を書いてください。

## 構成ルール
1. **即実行可能なコード (Ready-to-Run)**: import文から含めた完全なコード。
2. **バージョン・アップデート情報**: 言語バージョンアップに伴う推奨される書き方の変化。
3. **解説の深さ**: メモリ効率、スレッドセーフなどプロフェッショナルな視点。

## Zenn用Front Matter
---
title: "【Wiki】[技術テーマ名] (Java/C# 実装リファレンス)"
emoji: "🛠️"
type: "tech"
topics: ["java", "csharp", "新人教育", "architecture", "wiki"]
published: false
---
"""

def main():
    if not GOOGLE_API_KEY:
        print("Error: GEMINI_API_KEY is not set.")
        return

    print("Generating technical wiki article...")
    prompt = create_wiki_prompt()
    article_content = get_ai_response(prompt)

    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    directory = "articles"
    filename = f"{directory}/ref-{date_str}.md"

    os.makedirs(directory, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(article_content)
    
    print(f"Success: {filename} has been created!")

if __name__ == "__main__":
    main()