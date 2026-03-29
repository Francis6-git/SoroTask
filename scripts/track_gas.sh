#!/bin/bash
set -eo pipefail

echo "Running gas tracking tests..."

# CD into the contract directory where cargo can run
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR/../contract"

# Run the test_gas module tests, capture output
OUTPUT=$(cargo test test_gas --nocapture 2>&1 || true)

# Extract only lines that start with "GAS_TRACKER: "
echo "[" > ../gas_report.json
FIRST=true

while IFS= read -r line; do
  if [[ "$line" == GAS_TRACKER:* ]]; then
    JSON="${line#GAS_TRACKER: }"
    if [ "$FIRST" = true ]; then
      FIRST=false
    else
      echo "," >> ../gas_report.json
    fi
    echo "$JSON" >> ../gas_report.json
  fi
done <<< "$OUTPUT"

echo "]" >> ../gas_report.json

echo "Gas tracking complete. Output saved to gas_report.json"
