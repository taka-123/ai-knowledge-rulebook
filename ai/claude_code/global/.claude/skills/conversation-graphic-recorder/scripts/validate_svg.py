#!/usr/bin/env python3
"""Minimal validator for generated Conversation Graphic Recorder SVG files."""

from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

PLACEHOLDER = re.compile(r"\[[^\]\n]{1,100}\]|TODO|TBD|PLACEHOLDER", re.IGNORECASE)
EXTERNAL_REF = re.compile(r"(?:href|xlink:href)=[\"'](?:https?:)?//", re.IGNORECASE)
SCRIPT_TAG = re.compile(r"<\s*script\b", re.IGNORECASE)


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"ファイルが存在しません: {path}"]
    if path.suffix.lower() != ".svg":
        errors.append("拡張子が .svg ではありません")

    text = path.read_text(encoding="utf-8")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        return [f"XML解析エラー: {exc}"]

    if not root.tag.endswith("svg"):
        errors.append("ルート要素が <svg> ではありません")
    if not root.get("viewBox"):
        errors.append("viewBoxがありません")
    if not root.get("width") or not root.get("height"):
        errors.append("widthまたはheightがありません")
    if PLACEHOLDER.search(text):
        errors.append("プレースホルダーらしい文字列が残っています")
    if EXTERNAL_REF.search(text):
        errors.append("外部参照があります")
    if SCRIPT_TAG.search(text):
        errors.append("<script> は使用できません")

    texts = ["".join(node.itertext()).strip() for node in root.iter() if node.tag.endswith("text")]
    texts = [value for value in texts if value]
    if not texts:
        errors.append("テキスト要素がありません")
    if len(texts) > 45:
        errors.append(f"テキスト要素が多すぎます: {len(texts)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("svg", type=Path)
    args = parser.parse_args()

    errors = validate(args.svg)
    if errors:
        for error in errors:
            print(f"NG: {error}", file=sys.stderr)
        return 1

    print(f"OK: {args.svg}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
