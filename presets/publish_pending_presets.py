import hashlib
import json
import re
import sys
from pathlib import Path

COLOR_KEYS = {"idle", "ready", "printing", "complete", "paused", "error", "busy", "unknown", "bedHeating", "nozzleHeating", "bothHeating", "bedCooling", "nozzleCooling", "bothCooling", "zMotion", "setupAp", "startup"}
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 &'()+,.\-]{1,31}$")
HARDWARE_ID = re.compile(r"^[0-9a-f]{24}$")
ID = re.compile(r"^[0-9a-f-]{36}$")


def valid(preset: dict) -> bool:
    return (
        preset.get("schema") == 2
        and isinstance(preset.get("name"), str) and NAME.fullmatch(preset["name"])
        and isinstance(preset.get("description"), str) and 0 < len(preset["description"].encode()) <= 500
        and isinstance(preset.get("hardwareId"), str) and HARDWARE_ID.fullmatch(preset["hardwareId"])
        and isinstance(preset.get("colors"), dict) and set(preset["colors"]) == COLOR_KEYS
        and all(type(value) is int and 0 <= value <= 0xFFFFFF for value in preset["colors"].values())
    )


def main() -> None:
    pending_path, root, ids_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    pending = json.loads(pending_path.read_text(encoding="utf-8"))
    index_path = root / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if pending.get("schema") != 1 or index.get("schema") != 3 or index.get("maxPresets") != 200:
        raise ValueError("Invalid queue or catalogue schema")
    names = {entry["name"].casefold() for entry in index["presets"]}
    files = {entry["file"] for entry in index["presets"]}
    published = []
    for submission in pending.get("submissions", []):
        submission_id, preset = submission.get("id"), submission.get("preset")
        if not isinstance(submission_id, str) or not ID.fullmatch(submission_id) or not valid(preset):
            raise ValueError("Invalid queued submission")
        if preset["name"].casefold() in names or len(index["presets"]) >= 200:
            published.append(submission_id)
            continue
        slug = re.sub(r"[^a-z0-9]+", "-", preset["name"].lower()).strip("-")[:44] or "preset"
        file = f"files/{slug}-{preset['hardwareId'][:8]}.json"
        if file in files:
            file = f"files/{slug}-{submission_id[:8]}.json"
        document = {**preset, "submittedAt": submission["createdAt"]}
        raw = (json.dumps(document, indent=2) + "\n").encode()
        (root / file).write_bytes(raw)
        index["presets"].append({"name": preset["name"], "description": preset["description"], "hardwareId": preset["hardwareId"], "file": file, "sha256": hashlib.sha256(raw).hexdigest()})
        names.add(preset["name"].casefold()); files.add(file); published.append(submission_id)
    index["presets"].sort(key=lambda entry: entry["name"].casefold())
    index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    ids_path.write_text(json.dumps({"ids": published}), encoding="utf-8")


if __name__ == "__main__":
    main()
