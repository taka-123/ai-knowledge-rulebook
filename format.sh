#!/bin/bash
# 一括フォーマットスクリプト
# 使用法: ./format.sh [check|fix]

set -e

COLOR_RED='\033[0;31m'
COLOR_GREEN='\033[0;32m'
COLOR_YELLOW='\033[1;33m'
COLOR_BLUE='\033[0;34m'
COLOR_NC='\033[0m' # No Color

print_status() {
    echo -e "${COLOR_BLUE}[INFO]${COLOR_NC} $1"
}

print_success() {
    echo -e "${COLOR_GREEN}[SUCCESS]${COLOR_NC} $1"
}

print_warning() {
    echo -e "${COLOR_YELLOW}[WARNING]${COLOR_NC} $1"
}

print_error() {
    echo -e "${COLOR_RED}[ERROR]${COLOR_NC} $1"
}

# モード判定
MODE="${1:-check}"
if [[ "$MODE" != "check" && "$MODE" != "fix" ]]; then
    print_error "使用法: $0 [check|fix]"
    print_error "  check: 構文チェックのみ（デフォルト）"
    print_error "  fix:   自動修正を実行"
    exit 1
fi

print_status "🔧 一括フォーマット開始 (モード: $MODE)"
FAILED=0

# 必要なツールの確認
check_tool() {
    local tool="$1"
    local install_cmd="$2"
    local python_module="$3"

    # 通常のコマンドとして存在するかチェック
    if command -v "$tool" &> /dev/null; then
        return 0
    fi

    # Python moduleとして存在するかチェック
    if [[ -n "$python_module" ]] && python3 -m "$python_module" --version &> /dev/null; then
        return 0
    fi

    print_error "$tool がインストールされていません"
    print_error "インストール方法: $install_cmd"
    return 1
}

print_status "📋 必要なツールの確認中..."
# prettier と markdownlint-cli2 は npx 経由で使用するためチェックをスキップ
check_tool "yamllint" "pip3 install yamllint" "yamllint" || exit 1
check_tool "check-jsonschema" "pip3 install check-jsonschema" "check_jsonschema" || exit 1

if command -v check-jsonschema &> /dev/null; then
    CHECK_JSONSCHEMA_CMD=(check-jsonschema)
else
    CHECK_JSONSCHEMA_CMD=(python3 -m check_jsonschema)
fi

# Markdownフォーマット
print_status "📝 Markdownファイルの処理中..."
if [[ "$MODE" == "fix" ]]; then
    # Prettierで整形
    npx prettier --write "**/*.{md,markdown,mdx}" --ignore-path .prettierignore
    print_success "Markdownファイルを自動整形しました"
else
    # Prettierでチェック
    if npx prettier --check "**/*.{md,markdown,mdx}" --ignore-path .prettierignore; then
        print_success "Markdownファイルのフォーマットチェック: OK"
    else
        print_warning "Markdownファイルに問題があります（自動修正: ./format.sh fix）"
        FAILED=1
    fi
fi

# Markdownlint（品質チェック）
print_status "🔍 Markdownファイルの品質チェック中..."
if [[ "$MODE" == "fix" ]]; then
    MARKDOWNLINT_CMD=(npx markdownlint-cli2 --fix)
else
    MARKDOWNLINT_CMD=(npx markdownlint-cli2)
fi

if "${MARKDOWNLINT_CMD[@]}"; then
    print_success "Markdown品質チェック: OK"
else
    print_warning "Markdown品質に問題があります（自動修正: npm run fix:md）"
    FAILED=1
fi

# YAMLフォーマット
print_status "🗂️ YAMLファイルの処理中..."
if [[ "$MODE" == "fix" ]]; then
    # Prettierで整形
    npx prettier --write "**/*.{yml,yaml}" --ignore-path .prettierignore
    print_success "YAMLファイルを自動整形しました"
else
    # yamllintをpython moduleとして実行
    if command -v yamllint &> /dev/null; then
        YAMLLINT_CMD="yamllint"
    else
        YAMLLINT_CMD="python3 -m yamllint"
    fi

    if $YAMLLINT_CMD -c ./.config/.yamllint.yml .; then
        print_success "YAMLファイルの構文チェック: OK"
    else
        print_warning "YAMLファイルに問題があります（自動修正: ./format.sh fix）"
        FAILED=1
    fi
fi

# JSONフォーマット
print_status "📋 JSONファイルの処理中..."
if [[ "$MODE" == "fix" ]]; then
    npx prettier --write "**/*.{json,jsonc}" --ignore-path .prettierignore
    print_success "JSONファイルを自動整形しました"
else
    if npx prettier --check "**/*.{json,jsonc}" --ignore-path .prettierignore; then
        print_success "JSONファイルの構文チェック: OK"
    else
        print_warning "JSONファイルに問題があります（自動修正: ./format.sh fix）"
        FAILED=1
    fi
fi

# JavaScriptフォーマット
print_status "🧩 JavaScriptファイルの処理中..."
if [[ "$MODE" == "fix" ]]; then
    npx prettier --write "**/*.{js,mjs,cjs,ts,tsx,jsx}" --ignore-path .prettierignore
    print_success "JavaScriptファイルを自動整形しました"
else
    if npx prettier --check "**/*.{js,mjs,cjs,ts,tsx,jsx}" --ignore-path .prettierignore; then
        print_success "JavaScriptファイルのフォーマットチェック: OK"
    else
        print_warning "JavaScriptファイルに問題があります（自動修正: ./format.sh fix）"
        FAILED=1
    fi
fi

# JSON Schema検証（プロジェクト特有のファイルのみ）
print_status "🔍 JSON Schemaの検証中..."

# AI Profile Schema検証（プロファイル用JSONファイルのみ対象）
AI_PROFILE_FILES=$(find ai -name "*profile*.json" -type f 2>/dev/null)
if [[ -n "$AI_PROFILE_FILES" ]]; then
    if echo "$AI_PROFILE_FILES" | xargs "${CHECK_JSONSCHEMA_CMD[@]}" --schemafile schemas/ai_profile.schema.json 2>/dev/null; then
        print_success "AI Profile Schemaの検証: OK"
    else
        print_warning "AI Profile Schemaに問題があります"
        FAILED=1
    fi
else
    print_success "AI Profile JSON: 対象ファイルなし（*profile*.json）"
fi

# Notes Schema検証（notes用JSONファイルのみ対象）
NOTES_JSON_FILES=$(find notes -name "*.json" -not -name "*.jsonc" -type f 2>/dev/null)
if [[ -n "$NOTES_JSON_FILES" ]]; then
    if echo "$NOTES_JSON_FILES" | xargs "${CHECK_JSONSCHEMA_CMD[@]}" --schemafile schemas/notes.schema.json 2>/dev/null; then
        print_success "Notes Schemaの検証: OK"
    else
        print_warning "Notes Schemaに問題があります"
        FAILED=1
    fi
else
    print_success "Notes JSON: 対象ファイルなし"
fi

print_success "🎉 一括フォーマット完了!"

if [[ "$MODE" == "check" ]]; then
    print_status "💡 自動修正を実行する場合: ./format.sh fix"
fi

if [[ "$FAILED" -ne 0 ]]; then
    exit 1
fi