#!/usr/bin/env python3
"""Build the bounded OTA catalogue consumed by the lightbar firmware."""

import argparse
import datetime as dt
import json
from pathlib import Path


SCHEMA = 1
MAX_RELEASES = 50
MAX_NOTES_CHARS = 1200
MAX_OUTPUT_BYTES = 96 * 1024


def firmware_asset(release):
    tag = str(release.get("tag_name", ""))
    expected = f"core-one-lightbar-{tag}.bin"
    assets = release.get("assets") or []
    for asset in assets:
        if asset.get("name") == expected:
            return asset
    for asset in assets:
        name = str(asset.get("name", ""))
        if name.endswith(".bin") and "bootloader" not in name and "partitions" not in name:
            return asset
    return None


def build_catalogue(releases, generated_at):
    entries = []
    for release in releases:
        if release.get("draft"):
            continue
        asset = firmware_asset(release)
        asset_id = asset.get("id") if asset else None
        if not isinstance(asset_id, int) or asset_id <= 0:
            continue
        notes = str(release.get("body") or "").strip()
        if len(notes) > MAX_NOTES_CHARS:
            notes = notes[: MAX_NOTES_CHARS - 1].rstrip() + "…"
        entries.append({"tag": str(release.get("tag_name") or ""), "name": str(release.get("name") or ""), "publishedAt": str(release.get("published_at") or ""), "prerelease": bool(release.get("prerelease")), "notes": notes, "assetId": asset_id, "assetName": str(asset.get("name") or ""), "assetSize": int(asset.get("size") or 0)})
        if len(entries) >= MAX_RELEASES:
            break
    return {"schema": SCHEMA, "generatedAt": generated_at, "releases": entries}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--generated-at")
    args = parser.parse_args()
    releases = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(releases, list):
        raise SystemExit("release input must be a JSON array")
    generated_at = args.generated_at or dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")
    payload = json.dumps(build_catalogue(releases, generated_at), separators=(",", ":"), ensure_ascii=False) + "\n"
    if len(payload.encode("utf-8")) > MAX_OUTPUT_BYTES:
        raise SystemExit(f"catalogue exceeds {MAX_OUTPUT_BYTES} bytes")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(payload, encoding="utf-8")


if __name__ == "__main__":
    main()
