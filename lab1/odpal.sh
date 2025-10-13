#!/usr/bin/env bash
set -Eeuo pipefail

# Where inputs live: dane/N/*
INPUT_ROOT="dane"

# Output dirs
mkdir -p results logs timings

# Pick a timing command
if command -v /usr/bin/time >/dev/null 2>&1; then
  TIME_CMD="/usr/bin/time"
  TIME_FMT='%e\t%U\t%S\t%M\t%x'   # elapsed(s)  user(s)  sys(s)  maxRSS(KB)  exit
  USE_GNU_TIME=1
else
  TIME_CMD="time"                  # POSIX shell built-in; use -p and parse
  USE_GNU_TIME=0
fi

# Header for the timings table
TIMINGS_FILE="timings/timings.tsv"
echo -e "N\tfile\telapsed_s\tuser_s\tsys_s\tmax_rss_kb\texit_code" > "$TIMINGS_FILE"

for N in 0 1 2 3 4; do
  BIN="./zadanie${N}"
  if [[ ! -x "$BIN" ]]; then
    echo "warning: $BIN is missing or not executable, skipping" >&2
    continue
  fi

  shopt -s nullglob
  files=( "${INPUT_ROOT}/${N}/"* )
  shopt -u nullglob
  if (( ${#files[@]} == 0 )); then
    echo "warning: no inputs in ${INPUT_ROOT}/${N}/*, skipping" >&2
    continue
  fi

  for f in "${files[@]}"; do
    base="$(basename "$f")"
    out="results/zadanie${N}_${base}.out"
    err="logs/zadanie${N}_${base}.err"

    if (( USE_GNU_TIME )); then
      tmp="$(mktemp)"
      # time to tmp; program stdout to results, stderr to logs
      "$TIME_CMD" -f "$TIME_FMT" -o "$tmp" "$BIN" "$f" >"$out" 2>"$err" || true
      read -r elapsed user sys maxrss exitcode < "$tmp"
      rm -f "$tmp"
      echo -e "${N}\t${base}\t${elapsed}\t${user}\t${sys}\t${maxrss}\t${exitcode}" >> "$TIMINGS_FILE"
    else
      # Fallback: POSIX 'time -p' -> parse real/user/sys; RSS not available
      tmp="$(mktemp)"
      { time -p "$BIN" "$f" >"$out"; } 2>"$tmp" || true
      # Parse lines like: real 0.12\nuser 0.08\nsys 0.03
      real=$(awk '/^real/{print $2}' "$tmp")
      user=$(awk '/^user/{print $2}' "$tmp")
      sys=$(awk '/^sys/{print $2}' "$tmp")
      rm -f "$tmp"
      # We can’t get RSS/exit here; store placeholders
      echo -e "${N}\t${base}\t${real}\t${user}\t${sys}\tNA\tNA" >> "$TIMINGS_FILE"
      # stderr from the program itself isn’t captured with -p; if you want it:
      # rerun or redirect within the block above.
    fi

    echo "ran ${BIN} ${f} -> ${out}"
  done
done

echo "All done. See:"
echo "  - results/*.out   (program stdout)"
echo "  - logs/*.err      (program stderr)"
echo "  - ${TIMINGS_FILE} (tab-separated timings summary)"

