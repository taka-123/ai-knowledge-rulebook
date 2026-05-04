#!/bin/sh
# ~/.claude/statusline-command.sh
# Line 1: ~/cwd  branch  model
# Line 2: ctx: NN%used  5h: icon NN%used  7d: icon NN%used

input=$(cat)

json_value() {
  printf '%s' "$input" | jq -r "$1"
}

percent_int() {
  printf '%.0f' "$1"
}

append_segment() {
  if [ -n "$line2" ]; then
    line2="${line2}  $1"
  else
    line2="$1"
  fi
}

cwd=$(json_value '.workspace.current_dir // .cwd // ""')
short_cwd=$(echo "$cwd" | sed "s|^$HOME|~|")

model=$(json_value '.model.display_name // ""' \
  | sed -e 's/Claude //' \
        -e 's/ Sonnet$/S/' \
        -e 's/ Haiku$/H/' \
        -e 's/ Opus$/O/')

branch=""
if GIT_OPTIONAL_LOCKS=0 git -C "$cwd" rev-parse --git-dir >/dev/null 2>&1; then
  branch=$(GIT_OPTIONAL_LOCKS=0 git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null \
        || GIT_OPTIONAL_LOCKS=0 git -C "$cwd" rev-parse --short HEAD 2>/dev/null)
fi

ctx_used=$(json_value '.context_window.used_percentage // empty')
five_h=$(json_value '.rate_limits.five_hour.used_percentage // empty')
five_h_reset=$(json_value '.rate_limits.five_hour.resets_at // empty')
seven_d=$(json_value '.rate_limits.seven_day.used_percentage // empty')
seven_d_reset=$(json_value '.rate_limits.seven_day.resets_at // empty')

CYAN='\033[36m'
YELLOW='\033[33m'
MAGENTA='\033[35m'
GREEN='\033[32m'
RED='\033[31m'
DIM='\033[2m'
RESET='\033[0m'

# TrueColor gradient: green(0%) -> yellow(50%) -> red(100%)
gradient_color() {
  pct=$1
  if [ "$pct" -lt 50 ]; then
    r=$(( pct * 5 ))
    printf '\\033[38;2;%d;200;80m' "$r"
  else
    g=$(( 200 - (pct - 50) * 4 ))
    [ "$g" -lt 0 ] && g=0
    printf '\\033[38;2;255;%d;60m' "$g"
  fi
}

# Format seconds as "Xd Yh", "Xh Ym", or "Ym"
time_until() {
  secs=$(( $1 - $(date +%s) ))
  [ "$secs" -le 0 ] && return
  d=$(( secs / 86400 ))
  h=$(( (secs % 86400) / 3600 ))
  m=$(( (secs % 3600) / 60 ))
  if [ "$d" -gt 0 ]; then printf '%dd%dh' "$d" "$h"
  elif [ "$h" -gt 0 ]; then printf '%dh%dm' "$h" "$m"
  else printf '%dm' "$m"
  fi
}

# Ring meter: 5 levels (space-separated from number)
ring_icon() {
  pct=$1
  if   [ "$pct" -lt 13 ]; then printf '%s' '○'
  elif [ "$pct" -lt 38 ]; then printf '%s' '◔'
  elif [ "$pct" -lt 63 ]; then printf '%s' '◑'
  elif [ "$pct" -lt 88 ]; then printf '%s' '◕'
  else                          printf '%s' '●'
  fi
}

# --- Line 1: location info ---
line1="${CYAN}${short_cwd}${RESET}"
[ -n "$branch" ] && line1="${line1}  ${YELLOW}${branch}${RESET}"
[ -n "$model" ]  && line1="${line1}  ${MAGENTA}${model}${RESET}"

# --- Line 2: resource usage ---
line2=""

if [ -n "$ctx_used" ]; then
  ctx_int=$(percent_int "$ctx_used")
  if [ "$ctx_int" -lt 60 ]; then ctx_color="$GREEN"
  elif [ "$ctx_int" -lt 85 ]; then ctx_color="$YELLOW"
  else ctx_color="$RED"
  fi
  append_segment "${ctx_color}ctx: ${ctx_int}%${RESET}"
fi

if [ -n "$five_h" ]; then
  pct_int=$(percent_int "$five_h")
  col=$(gradient_color "$pct_int")
  icon=$(ring_icon "$pct_int")
  seg="${DIM}5h:${RESET} ${col}${icon} ${pct_int}%${RESET}"
  if [ -n "$five_h_reset" ]; then
    t=$(time_until "$five_h_reset")
    [ -n "$t" ] && seg="${seg}${DIM}(${t})${RESET}"
  fi
  append_segment "$seg"
fi

if [ -n "$seven_d" ]; then
  pct_int=$(percent_int "$seven_d")
  col=$(gradient_color "$pct_int")
  icon=$(ring_icon "$pct_int")
  seg="${DIM}7d:${RESET} ${col}${icon} ${pct_int}%${RESET}"
  if [ "$pct_int" -gt 70 ] && [ -n "$seven_d_reset" ]; then
    t=$(time_until "$seven_d_reset")
    [ -n "$t" ] && seg="${seg}${DIM}(${t})${RESET}"
  fi
  append_segment "$seg"
fi

printf '%b\n' "$line1"
if [ -n "$line2" ]; then
  printf '%b' "$line2"
fi
