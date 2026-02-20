import os
import datetime
from google import genai

# GitHub SecretsからAPIキーを読み込む
GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

# クライアントの初期化（api_version: 'v1' を指定）
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

    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    directory = "articles"
    filename = f"{directory}/log-{date_str}.md"

    os.makedirs(directory, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        f.write(article_content)
    
    print(f"Success: {filename} has been created!")

if __name__ == "__main__":
    main()