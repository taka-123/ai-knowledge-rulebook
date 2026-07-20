#!/usr/bin/env python3
"""Minimal validator for generated Conversation Visualizer HTML."""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}
PLACEHOLDER_PATTERNS = (
    re.compile(r"\[[^\]\n]{1,80}\]"),
    re.compile(r"TODO|TBD|PLACEHOLDER", re.IGNORECASE),
)


class StructuralParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        return

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_TAGS:
            return
        if not self.stack:
            self.errors.append(f"余分な終了タグ: </{tag}>")
            return
        if self.stack[-1] == tag:
            self.stack.pop()
            return
        if tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.errors.append(
                    f"閉じ順が不正: <{self.stack[-1]}> の前に </{tag}>"
                )
                self.stack.pop()
            if self.stack:
                self.stack.pop()
        else:
            self.errors.append(f"対応する開始タグがない: </{tag}>")


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"ファイルが存在しません: {path}"]
    if path.suffix.lower() not in {".html", ".htm"}:
        errors.append("拡張子が .html / .htm ではありません")

    text = path.read_text(encoding="utf-8")
    if "<!doctype html>" not in text.lower():
        errors.append("DOCTYPEがありません")
    if 'lang="ja"' not in text and "lang='ja'" not in text:
        errors.append("<html lang=\"ja\"> がありません")
    if "charset=\"utf-8\"" not in text.lower() and "charset='utf-8'" not in text.lower():
        errors.append("UTF-8 charset指定がありません")

    for pattern in PLACEHOLDER_PATTERNS:
        match = pattern.search(text)
        if match:
            errors.append(f"プレースホルダーらしい文字列が残っています: {match.group(0)}")
            break

    parser = StructuralParser()
    try:
        parser.feed(text)
        parser.close()
    except Exception as exc:  # HTMLParser errors are rare but should be reported.
        errors.append(f"HTML解析エラー: {exc}")
    errors.extend(parser.errors)
    if parser.stack:
        errors.append("未終了タグ: " + ", ".join(f"<{tag}>" for tag in parser.stack[-10:]))

    if re.search(r"<(section|article|div)[^>]*>\s*</\1>", text, re.IGNORECASE):
        errors.append("空のコンテナ要素があります")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", type=Path)
    args = parser.parse_args()

    errors = validate(args.html)
    if errors:
        for error in errors:
            print(f"NG: {error}", file=sys.stderr)
        return 1

    print(f"OK: {args.html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
