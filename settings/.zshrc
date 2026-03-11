# ==================================================
# 基本設定（最初に設定すべき項目）
# ==================================================

# 日本語環境設定（ターミナルでの日本語入力問題を解決）
export LANG=en_US.UTF-8
export LC_CTYPE=ja_JP.UTF-8 # 文字処理のみ日本語

# ターミナル固有の設定（OSCクエリ問題の追加対策）
if [[ "$TERM_PROGRAM" == "vscode" ]] || [[ "$TERM_PROGRAM" == "cursor" ]]; then
  export TERM_NO_OSC=1
fi

# ==================================================
# 補完システムの初期化（1回だけ実行）
# ==================================================

autoload -Uz compinit
# compinit の遅延読み込み化と重複排除
if [ $(date +'%j') != $(/usr/bin/stat -f '%Sm' -t '%j' ${ZDOTDIR:-$HOME}/.zcompdump 2>/dev/null || echo 0) ]; then
  compinit
else
  compinit -C
fi

# ==================================================
# zplug設定
# ==================================================

# Homebrewのインストール先（Apple Silicon/Intel）に応じてzplugのパスを自動設定
export ZPLUG_HOME=$(brew --prefix)/opt/zplug
export ZPLUG_REPOS=~/.zplug/repos
export ZPLUG_CACHE_DIR=~/.zplug/cache
export ZPLUG_LOG_DIR=~/.zplug/log
export ZPLUG_BIN=/opt/homebrew/opt/zplug/bin
if [[ -s $ZPLUG_HOME/init.zsh ]]; then
  source $ZPLUG_HOME/init.zsh

  # zplugの設定を最適化
  zplug 'zplug/zplug', hook-build:'zplug --self-manage', defer:0
  zplug "mafredri/zsh-async", defer:0

  # pureテーマの設定（OSCクエリ問題対策含む）
  zplug "sindresorhus/pure", use:pure.zsh, from:github, as:theme, defer:0 && {
    export PURE_PROMPT_SYMBOL="❯❯❯"
    # OSCクエリ無効化（10;rgb問題の根本解決）
    export PURE_GIT_PULL=0
    export PURE_GIT_UNTRACKED_DIRTY=0
    export PURE_CMD_MAX_EXEC_TIME=0
    # ターミナルタイトル更新も無効化
    export PURE_GIT_DOWN_ARROW=""
    export PURE_GIT_UP_ARROW=""
  }

  zplug "zsh-users/zsh-completions", defer:0
  zplug "b4b4r07/enhancd", use:init.sh, defer:1
  zplug "zsh-users/zsh-syntax-highlighting", defer:2
  zplug "zsh-users/zsh-history-substring-search", defer:3

  # インストールと読み込み
  if ! zplug check --verbose; then
    printf "インストールしますか？[y/N]: "
    if read -q; then
      echo
      zplug install
    fi
  fi
  zplug load
fi

# ==================================================
# 開発環境設定
# ==================================================

# --- バージョン管理ツール ---

# mise設定（Node.js、Python、Ruby等の統合管理）
if command -v mise &> /dev/null; then
  eval "$(mise activate zsh)"
fi

# --- Python関連 ---
# Conda（miseと併用可能）
# Anacondaのインストール先は環境により異なる場合があるため注意
# (例: /opt/anaconda3, ~/opt/anaconda3, /usr/local/anaconda3など)
if [ -f "/opt/anaconda3/etc/profile.d/conda.sh" ]; then
  . "/opt/anaconda3/etc/profile.d/conda.sh"
else
  export PATH="/opt/anaconda3/bin:$PATH"
fi

# --- コンテナ関連 ---
export DOCKER_DEFAULT_PLATFORM=linux/amd64
# Docker補完
if [ -d "$HOME/.docker/completions" ]; then
  fpath=($HOME/.docker/completions $fpath)
fi

# --- 開発ツール ---
# local bin
export PATH="$HOME/.local/bin:$PATH"
# Windsurf設定
export PATH="$HOME/.codeium/windsurf/bin:$PATH"
# bun
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# ==================================================
# 履歴設定
# ==================================================

export HISTFILE=~/.zsh_history
export HISTSIZE=100000
export SAVEHIST=100000

# ==================================================
# zshオプション
# ==================================================

setopt no_beep
setopt auto_pushd
setopt pushd_ignore_dups
setopt auto_cd
setopt hist_ignore_dups
setopt hist_ignore_all_dups
setopt hist_save_no_dups
setopt share_history
setopt inc_append_history
setopt hist_verify
setopt extended_history   # タイムスタンプ付き履歴
setopt hist_reduce_blanks # 余分な空白を削除

# ==================================================
# エイリアス
# ==================================================

# エディタ
alias vi="nvim"
alias vim="nvim"
alias view="nvim -R"

# 基本コマンド
alias ls="ls -F"
alias ll="ls -la"
alias mkdir="mkdir -p"

# 安全なファイル削除（ゴミ箱に移動）
alias rm="trash"

# 英語マニュアル
alias eman="env LANG=C man"

# Claude Code 関連
alias cmp="claude-monitor --timezone Asia/Tokyo --plan pro"
alias cmm="claude-monitor --timezone Asia/Tokyo --plan max5"

# --- AI CLI Agents (ターミナル内対話・自動生成) ---
alias cl="claude"
alias ca="cursor-agent"
alias cx="codex"
alias gm="gemini"

# --- AI IDE Launchers (GUIエディタ起動) ---
alias ws="windsurf"
alias km="kamui"

# --- difit (AI差分レビュー) ---
# 1. 作業中の全変更をレビュー（未追跡ファイル含む）
alias dif='npx difit . --clean --keep-alive --include-untracked'
# 2. リモートのデフォルトブランチ（main/master）と現在の作業状態の差分をレビュー
# ※ origin/HEAD を使うことでブランチ名の揺れを自動吸収します
alias difm='npx difit origin/HEAD . --clean --keep-alive'
# 3. 過去のコミット履歴からfzfで2点間を選択してレビュー（AI生成コードの過去比較用）
alias diffzf='git log --oneline --decorate -100 | fzf | awk "{print $1}" | xargs -I {} npx difit {}~1 {} --clean --keep-alive'

# Laravel開発
alias sail="./vendor/bin/sail"
alias pint="./vendor/bin/pint -v"
alias larastan="./vendor/bin/phpstan analyse --memory-limit=512M"

# その他
alias gkey="oathtool --totp --base32 kzoypornhcwgantede6h5u73ncmy3mnn"

# ==================================================
# 便利な関数
# ==================================================

# fzfを使ったディレクトリ移動
fd() {
  local dir
  dir=$(find ${1:-.} -path '*/\.*' -prune \
    -o -type d -print 2>/dev/null | fzf +m) &&
    cd "$dir"
}

# fzfを使ったブランチ切り替え
fbr() {
  local branches branch
  branches=$(git --no-pager branch -vv) &&
    branch=$(echo "$branches" | fzf +m) &&
    git checkout $(echo "$branch" | awk '{print $1}' | sed "s/.* //")
}

# 日本語入力デバッグ用（問題が発生した時用）
check-locale() {
  echo "=== Current Locale Settings ==="
  locale
  echo "\n=== Terminal Info ==="
  echo "TERM: $TERM"
  echo "TERM_PROGRAM: $TERM_PROGRAM"
  echo "iTerm2 Profile: $ITERM_PROFILE"
}

# ==================================================
# AIツール用設定
# ==================================================

# ページャー無効化（AIツールがqで止まらないように）
export GIT_PAGER=""
export GH_PAGER=""
export PAGER=""
export LESS="-F -X"

# Git対話モード簡略化
export GIT_MERGE_AUTOEDIT=no

# AIツール判定用（より詳細な出力制御）
if [[ "$TERM_PROGRAM" == "cursor" ]] || [[ -n "$CLAUDE_CODE" ]] || [[ -n "$WINDSURF" ]]; then
  # AIツール内では更にシンプルな表示
  export GIT_PAGER="cat"
  alias git="git --no-pager"
fi

# ==================================================
# ローカル設定の読み込み（最後に実行）
# ==================================================

if [[ -f ~/.zshrc.local ]]; then
  source ~/.zshrc.local
fi

[[ "$TERM_PROGRAM" == "kiro" ]] && . "$(kiro --locate-shell-integration-path zsh)"

# Added by Antigravity
export PATH="~/.antigravity/antigravity/bin:$PATH"
eval "$(/opt/homebrew/bin/brew shellenv)"

# bun completions
[ -s "~/.bun/_bun" ] && source "~/.bun/_bun"
alias rm=gomi
