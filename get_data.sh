#!/bin/bash
# Fetch the tahini ATR-FTIR data (CC BY 4.0) released with Batayhi et al., Foods 2026, 15, 3639,
# at the commit used for this study. Archived copy: https://doi.org/10.5281/zenodo.21446757
set -e
cd "$(dirname "$0")"
[ -d source_repo ] || git clone https://github.com/abdulhamidbatayhi123/kanfood-tahini-mango- source_repo
git -C source_repo checkout 3004a07e4b09c56036387d5e5c50ca8f8a5ed839
sha256sum source_repo/data/tahini/Tahin_Aycicek1.xlsx 2>/dev/null || true
echo "expected sha256: 75b4549a1cc7735dba1fb90936e2f659c17c2ed9fb94cfdb17023b3c927da257"
