#!/usr/bin/env python3
import json
import sys
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "llms-config.json"
INDEX_PATH = ROOT / "llms.txt"
FULL_PATH = ROOT / "llms-full.txt"
SIZE_BUDGET = 600_000

spec = importlib.util.spec_from_file_location("build_llms", ROOT / "scripts" / "build-llms.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

config = json.loads(CONFIG_PATH.read_text())
errors = []

for item in config["files"]:
    path = ROOT / item["path"]
    if not path.exists():
        errors.append(f"Missing source file: {item['path']}")

expected_index = mod.render_index(config)
expected_full = mod.render_full(config)

if not INDEX_PATH.exists() or INDEX_PATH.read_text() != expected_index:
    errors.append("llms.txt is stale. Run: python3 scripts/build-llms.py")

if not FULL_PATH.exists() or FULL_PATH.read_text() != expected_full:
    errors.append("llms-full.txt is stale. Run: python3 scripts/build-llms.py")

if FULL_PATH.exists() and FULL_PATH.stat().st_size > SIZE_BUDGET:
    errors.append(f"llms-full.txt exceeds size budget of {SIZE_BUDGET} bytes")

if errors:
    for err in errors:
        print(f"ERROR: {err}")
    sys.exit(1)

print("llms docs OK")
