#!/usr/bin/env python3
import json
import sys
import os

def load_json(filepath):
    if not os.path.exists(filepath):
        return {}
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            # convert list of dicts to dict keyed by function
            return {item['function']: item for item in data}
    except Exception as e:
        print(f"Error loading {filepath}: {e}", file=sys.stderr)
        return {}

def format_diff(old, new):
    if old == 0:
        if new == 0:
            return "0 (0.00%)"
        return f"+{new} (+\u221E%)"
    diff = new - old
    pct = (diff / old) * 100
    sign = "+" if diff > 0 else ""
    return f"{sign}{diff} ({sign}{pct:.2f}%)"

def main():
    if len(sys.argv) < 3:
        print("Usage: compare_gas.py <base_json> <pr_json>", file=sys.stderr)
        sys.exit(1)

    base_path = sys.argv[1]
    pr_path = sys.argv[2]

    base_data = load_json(base_path)
    pr_data = load_json(pr_path)

    if not base_data and not pr_data:
        print("No gas metrics found in either branch.", file=sys.stderr)
        sys.exit(0)

    all_funcs = sorted(list(set(base_data.keys()) | set(pr_data.keys())))

    output = []
    output.append("## \u26fd Gas Consumption Changes")
    output.append("")
    output.append("| Function | CPU Instructions | Diff (CPU) | Memory Bytes | Diff (Mem) |")
    output.append("|---|---|---|---|---|")

    for func in all_funcs:
        base_item = base_data.get(func, {"cpu": 0, "mem": 0})
        pr_item = pr_data.get(func, {"cpu": 0, "mem": 0})

        cpu_diff = format_diff(base_item["cpu"], pr_item["cpu"])
        mem_diff = format_diff(base_item["mem"], pr_item["mem"])

        # Highlight regressions in bold
        if pr_item["cpu"] > base_item["cpu"]:
            cpu_diff = f"**{cpu_diff}**"
        if pr_item["mem"] > base_item["mem"]:
            mem_diff = f"**{mem_diff}**"

        output.append(f"| `{func}` | {pr_item['cpu']} | {cpu_diff} | {pr_item['mem']} | {mem_diff} |")

    output.append("")
    output.append("*(Metrics are derived from native Rust execution approximations and track relative changes.)*")
    
    print("\n".join(output))

if __name__ == "__main__":
    main()
