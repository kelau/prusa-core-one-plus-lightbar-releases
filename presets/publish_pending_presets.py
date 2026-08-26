import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

COLOR_KEYS = {"idle", "ready", "printing", "complete", "paused", "error", "busy", "unknown", "bedHeating", "nozzleHeating", "bothHeating", "bedCooling", "nozzleCooling", "bothCooling", "zMotion", "setupAp", "startup"}
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 &'()+,.\-]{1,31}$")
HARDWARE_ID = re.compile(r"^[0-9a-f]{24}$")
ID = re.compile(r"^[0-9a-f-]{36}$")
FILE = re.compile(r"^files/[a-z0-9-]{1,64}\.json$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def valid_timestamp(value: object) -> bool:
    if not isinstance(value, str) or not value.endswith("Z"):
        return False
    try:
        datetime.fromisoformat(value[:-1] + "+00:00")
        return True
    except ValueError:
        return False


def valid(preset: dict) -> bool:
    return (
        preset.get("schema") == 2
        and isinstance(preset.get("name"), str) and NAME.fullmatch(preset["name"])
        and isinstance(preset.get("description"), str) and 0 < len(preset["description"].encode()) <= 500
        and isinstance(preset.get("hardwareId"), str) and HARDWARE_ID.fullmatch(preset["hardwareId"])
        and isinstance(preset.get("colors"), dict) and set(preset["colors"]) == COLOR_KEYS
        and all(type(value) is int and 0 <= value <= 0xFFFFFF for value in preset["colors"].values())
    )


def valid_index_entry(entry: object) -> bool:
    return (
        isinstance(entry, dict)
        and isinstance(entry.get("name"), str) and NAME.fullmatch(entry["name"])
        and isinstance(entry.get("description"), str) and len(entry["description"].encode()) <= 500
        and (entry.get("hardwareId") in {"builtin", "legacy"} or isinstance(entry.get("hardwareId"), str) and HARDWARE_ID.fullmatch(entry["hardwareId"]))
        and valid_timestamp(entry.get("submittedAt"))
        and isinstance(entry.get("file"), str) and FILE.fullmatch(entry["file"])
        and isinstance(entry.get("sha256"), str) and SHA256.fullmatch(entry["sha256"])
    )


def main() -> None:
    pending_path, root, ids_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    pending = json.loads(pending_path.read_text(encoding="utf-8"))
    index_path = root / "index.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if pending.get("schema") != 1 or index.get("schema") != 3 or index.get("maxPresets") != 200:
        raise ValueError("Invalid queue or catalogue schema")
    if not isinstance(index.get("presets"), list) or len(index["presets"]) > 200 or any(not valid_index_entry(entry) for entry in index["presets"]):
        raise ValueError("Invalid catalogue entry")
    index["presets"] = [entry for entry in index["presets"] if (root / entry["file"]).is_file()]
    names = {entry["name"].casefold() for entry in index["presets"]}
    files = {entry["file"] for entry in index["presets"]}
    published = []
    for submission in pending.get("submissions", []):
        submission_id, preset = submission.get("id"), submission.get("preset")
        submitted_at = submission.get("createdAt")
        if not isinstance(submission_id, str) or not ID.fullmatch(submission_id) or not valid(preset) or not valid_timestamp(submitted_at):
            raise ValueError("Invalid queued submission")
        if preset["name"].casefold() in names or len(index["presets"]) >= 200:
            published.append(submission_id)
            continue
        slug = re.sub(r"[^a-z0-9]+", "-", preset["name"].lower()).strip("-")[:44] or "preset"
        file = f"files/{slug}-{preset['hardwareId'][:8]}.json"
        if file in files:
            file = f"files/{slug}-{submission_id[:8]}.json"
        document = {**preset, "submittedAt": submitted_at}
        raw = (json.dumps(document, indent=2) + "\n").encode()
        (root / file).write_bytes(raw)
        index["presets"].append({"name": preset["name"], "description": preset["description"], "hardwareId": preset["hardwareId"], "submittedAt": submitted_at, "file": file, "sha256": hashlib.sha256(raw).hexdigest()})
        names.add(preset["name"].casefold()); files.add(file); published.append(submission_id)
    index["presets"].sort(key=lambda entry: entry["name"].casefold())
    index_path.write_text(json.dumps(index, indent=2) + "\n", encoding="utf-8")
    ids_path.write_text(json.dumps({"ids": published}), encoding="utf-8")


if __name__ == "__main__":
    main()
