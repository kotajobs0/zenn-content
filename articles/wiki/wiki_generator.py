import os
import datetime
from dotenv import load_dotenv
import google.genai as genai

# 1. .envファイルの内容を環境変数として読み込む
load_dotenv()

# 2. 環境変数から値を取り出す
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 3. クライアントを初期化
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
    
    # --- が最初に出てくる位置を探す
    start_index = text.find('---')
    if start_index != -1:
        # --- より前の部分だけバッククォートを除去（Front Matter前のゴミ掃除）
        before = text[:start_index].replace('```markdown', '').replace('```yaml', '').replace('```', '')
        # --- 以降（Front Matter + 記事本文）はそのまま残す
        text = before + text[start_index:]

    # 先頭の空白・改行を除去して --- から始まるようにする
    text = text.strip()

    return text

def create_prompt():
    return """
あなたは、チームの技術標準を策定するリードエンジニアとして、若手が「そのまま実行できる」Zenn形式の技術リファレンス（Wiki）を書いてください。

## 構成ルール
1. **即実行可能なコード (Ready-to-Run)**: import文から含めた完全なコード。
2. **バージョン・アップデート情報**: 言語バージョンアップに伴う推奨される書き方の変化。
3. **解説の深さ**: メモリ効率、スレッドセーフなどプロフェッショナルな視点。

## Zenn用Front Matterの形式
記事の冒頭には、以下の形式のFront Matterを必ず含めてください。
バッククォートやコードブロック記法で囲まず、そのままの形式で出力してください。

---
title: "【Wiki】[技術テーマ名] (Java/C# 実装リファレンス)"
emoji: "🛠️"
type: "tech"
topics: ["java", "csharp", "新人教育", "architecture", "wiki"]
published: false
---

上記の --- で始まり --- で終わる部分が、記事の一番最初にそのまま来るように出力してください。
"""

def main():
    if not GOOGLE_API_KEY:
        print("Error: GEMINI_API_KEY is not set.")
        return
# このファイルがある articles/wiki フォルダ
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # articles/wiki から 1つ上に上がり(articles)、data/refs へ進む
    output_dir = os.path.normpath(os.path.join(script_dir, "..", "data", "refs"))
    
    # フォルダを作成
    os.makedirs(output_dir, exist_ok=True)

    print("Generating Wiki content...")
    prompt = create_prompt()
    article_content = get_ai_response(prompt)

    # ファイル名の生成 (Wiki用なので ref- から始める)
    now = datetime.datetime.now()
    date_str = now.strftime('%Y-%m-%d-%H%M%S')
    filename = f"ref-{date_str}.md"

    # 最終的な保存先フルパス
    full_save_path = os.path.join(output_dir, filename)

    # 保存実行
    with open(full_save_path, "w", encoding="utf-8") as f:
        f.write(article_content)
    
    print(f"Success: {full_save_path} has been created!")

if __name__ == "__main__":
    main()