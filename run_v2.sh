#!/bin/bash
# A2 rerun: lot-out folds in parallel (2 threads each, at most $MAXJ at once), then hold-out and random.
cd "$(dirname "$0")/src"
MAXJ=${MAXJ:-2}
run() { TORCH_THREADS=2 python s01_run.py "$@" > "../results/log_$(echo "$@" | tr ' ' '_').txt" 2>&1 && touch "../results/$(echo "$@" | tr ' ' '_').ok"; }
for job in "lolo chem T2" "lolo chem T3" "lolo chem T4" "lolo chem T5" "holdout chem" "random chem"; do
  ok="../results/$(echo $job | tr ' ' '_').ok"; [ -f "$ok" ] && continue
  while [ "$(jobs -rp | wc -l)" -ge "$MAXJ" ]; do sleep 30; done
  echo "start $job $(date)"; run $job &
done
wait; echo "ALLDONE $(date)"
