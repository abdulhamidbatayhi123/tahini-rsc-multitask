#!/bin/bash
# Sequential runner with skip-on-.ok restart. One job at a time (shared, RAM-limited machine).
cd "$(dirname "$0")/src"
for cfg in "holdout chem" "lolo chem" "random chem" "holdout full" "lolo full" "random full" "lolo chemsnv" "lolo chem700"; do
  set -- $cfg
  ok="../results/$1_$2.ok"
  [ -f "$ok" ] && { echo "skip $cfg"; continue; }
  echo "start $cfg $(date)"
  if python s01_run.py $1 $2 > "../results/log_$1_$2.txt" 2>&1; then touch "$ok"; echo "done $cfg $(date)"; else echo "FAILED $cfg $(date)"; fi
done
echo ALLDONE
