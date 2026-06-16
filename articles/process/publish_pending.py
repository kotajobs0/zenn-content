# publish_pending.py
# published: false の記事を古い順に1本だけ published: true に変更してpushする
#
# 【使い方】
#   cd /c/.github/zenn-content
#   py -3 -X utf8 articles/process/publish_pending.py
#
# 【運用方針】
#   - 新規記事生成: daily_article.py
#   - 下書き記事の公開: publish_pending.py
#   毎日どちらかを実行して1日1本ペースを維持する

import subprocess
import re
from pathlib import Path

ARTICLES_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = ARTICLES_DIR.parent


def find_pending_articles() -> list[Path]:
    """published: false の記事を古い順に返す"""
    pending = []
    for md in sorted(ARTICLES_DIR.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        if "published: false" in text:
            pending.append(md)
    return pending


def publish(filepath: Path):
    """published: false → published: true に書き換える"""
    text = filepath.read_text(encoding="utf-8")
    updated = text.replace("published: false", "published: true", 1)
    filepath.write_text(updated, encoding="utf-8")


def git_push(filepath: Path, title: str):
    try:
        subprocess.run(["git", "add", str(filepath)], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "commit", "-m", f"feat: Zenn記事を公開「{title}」"], cwd=REPO_DIR, check=True)
        subprocess.run(["git", "push", "--set-upstream", "origin", "main"], cwd=REPO_DIR, check=True)
        print("✅ GitHubにpush完了 → Zennに自動反映されます")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ git操作でエラー: {e}")


def extract_title(filepath: Path) -> str:
    for line in filepath.read_text(encoding="utf-8").splitlines():
        if line.startswith("title:"):
            return line.replace("title:", "").strip().strip('"')
    return filepath.stem


def main():
    pending = find_pending_articles()

    if not pending:
        print("✅ 下書き記事はありません。daily_article.py で新規記事を生成してください。")
        return

    print(f"📋 下書き記事: {len(pending)}本")
    for i, p in enumerate(pending, 1):
        title = extract_title(p)
        print(f"  {i}. {p.name} → {title}")

    target = pending[0]
    title = extract_title(target)
    print(f"\n▶ 公開する記事: 「{title}」")

    publish(target)
    git_push(target, title)

    remaining = len(pending) - 1
    print(f"\n残り下書き: {remaining}本")
    if remaining > 0:
        next_title = extract_title(pending[1])
        print(f"次回: 「{next_title}」")


if __name__ == "__main__":
    main()
