#!/bin/bash
# A2 full-range sensitivity runs (2 threads each, at most $MAXJ at once), then hold-out and random.
cd "$(dirname "$0")/src"
MAXJ=${MAXJ:-2}
run() { TORCH_THREADS=2 python s01_run.py "$@" > "../results/log_$(echo "$@" | tr ' ' '_').txt" 2>&1 && touch "../results/$(echo "$@" | tr ' ' '_').ok"; }
for job in "lolo full T1" "lolo full T2" "lolo full T3" "lolo full T4" "lolo full T5" "holdout full" "random full"; do
  ok="../results/$(echo $job | tr ' ' '_').ok"; [ -f "$ok" ] && continue
  while [ "$(jobs -rp | wc -l)" -ge "$MAXJ" ]; do sleep 30; done
  echo "start $job $(date)"; run $job &
done
wait; echo "ALLDONE $(date)"
