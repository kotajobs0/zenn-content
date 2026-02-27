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
    
    text = text.replace('```markdown', '')
    text = text.replace('```yaml', '')
    text = text.replace('```', '')
    
    # ---が最初に出てくる位置からを記事本文として取得
    start_index = text.find('---')
    if start_index != -1:
        text = text[start_index:]
    return text

def create_prompt():
    return """
あなたは、チームの技術標準を策定するリードエンジニアとして、若手が「そのまま実行できる」Zenn形式の技術リファレンス（Wiki）を書いてください。

## 構成ルール
1. **即実行可能なコード (Ready-to-Run)**: import文から含めた完全なコード。
2. **バージョン・アップデート情報**: 言語バージョンアップに伴う推奨される書き方の変化。
3. **解説の深さ**: メモリ効率、スレッドセーフなどプロフェッショナルな視点。

## Zenn用Front Matter

title: "【Wiki】[技術テーマ名] (Java/C# 実装リファレンス)"
emoji: "🛠️"
type: "tech"
topics: ["java", "csharp", "新人教育", "architecture", "wiki"]
published: false

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
    date_str = now.strftime('%Y-%m-%d_%H%M%S')
    filename = f"ref-{date_str}.md"

    # 最終的な保存先フルパス
    full_save_path = os.path.join(output_dir, filename)

    # 保存実行
    with open(full_save_path, "w", encoding="utf-8") as f:
        f.write(article_content)
    
    print(f"Success: {full_save_path} has been created!")

if __name__ == "__main__":
    main()